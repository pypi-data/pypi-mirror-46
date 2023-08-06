import requests
import json
import re
import os
import time
import pyodbc
import pandas as pd
import logging
from datetime import datetime, timezone
from calendar import monthrange

from requests.exceptions import ConnectionError
from urllib3.exceptions import ProtocolError
from http.client import RemoteDisconnected

class db_updater:
    """Executes methods for updating a database of Samanage incidents as well as summarizing them.

    Args:
        debug (bool): if True, debug statements will be logged and (eventually) changes will only be made to debug server (default: False)

    Attributes:
        debug (bool): whether the updater is in debug mode
        headers (dict): header values to be used in making Samanage API requests
        server (string): the name of the SQL server to connect to
        database (string): the name of the database to update
        username (string): SQL server username
        password (string): SQL server password
        cnxn (pyodbc.connection): connection to SQL server established using above parameters
        cursor (pyodbc.cursor): for executing changes to the SQL database
        tables (dict): a dictionary giving the addresses of the database tables the updater will work with 
        new_tickets (int): count of tickets that were added to the DB by this object
        updated_tickets (int): count of tickets that were updated in the DB by this object
    """

    def __init__(self, debug = False):
        self.debug = debug
        # set local environment vars for local debugging
        if debug:
            logging.basicConfig(level = logging.DEBUG)
            set_environment_vars()
        else:
            logging.basicConfig(level = logging.INFO)

        self.headers = {
            "Accept" : "application/vnd.samanage.v2.1+json",
            "Content-Type" : "application/json",
            "X-Samanage-Authorization" : os.environ['X_Samanage_Authorization']
        }
        # TODO we probably don't need to store these values on their own, just use them in the connection string?
        self.server = os.environ['db_server']
        self.database = os.environ['db_name']
        self.username = os.environ['db_username']
        self.password = os.environ['db_password']
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        self.cursor = self.cnxn.cursor()

        table_names = ["ticket_info", "weekly_in_queue", "monthly_in_queue", "monthly_created", "monthly_closed", "monthly_counts"]
        target_names = [self.database + ".dbo." + table for table in table_names]
        self.tables = dict(zip(table_names, target_names))
        
        self.new_tickets = 0
        self.updated_tickets = 0

    def get_response_links(self, response):
        """Retrieves the page links from an HTTP response.

        Args:
            response (requests.response): response from an HTTP GET request

        Returns:
            dict: the page links from the response
        """
        link_string = response.headers['Link']
        links = re.split(",", link_string)

        urls = []
        keys = []

        # link headers are formatted:
        # <https://api.samanage.com/incidents.json?layout=long&page=1>; rel="first"

        for link in links:
            split = re.split(';', link)

            url = re.search('<(.*)>', split[0])
            urls.append(url.group(1))

            key = re.search('"(.*)"', split[1])
            keys.append(key.group(1))

        links_dict = dict(zip(keys, urls))

        return links_dict

    def get_page(self, url, headers = None, payload = None):
        """Performs a GET request and returns the result as well as the next page, if it exists.

        Args:
            url (string): the URL for the request
            headers (dict): headers to pass with the request (default is object param headers)
            payload (dict): parameters for the request (default is None)

        Returns:
            list of strings: all JSON objects returned by the request
            string: the URL of the next page, or None if there is no next page
        """
        # use object headers by default
        if headers is None:
            headers = self.headers

        response = None
        retry_count = 0

        # connection is sometimes refused without warning; if this happens, wait a few minutes and try again
        while not response and retry_count < 5:
            try:
                response = requests.get(url, headers = headers, params = payload)
            except (RemoteDisconnected, ProtocolError, ConnectionError):
                current_time = datetime.datetime.now()
                next_time = current_time + datetime.timedelta(minutes = 5)
                logging.info("Remote connection closed at " + str(current_time) + ", retrying at " + str(next_time))
                retry_count += 1
                time.sleep(300)

        # TODO this needs to be handled elsewhere
        if not response:
            logging.error("Connection to Samanage API could not be re-established.")
            return None

        time.sleep(5)

        links = self.get_response_links(response)

        next_link = links['next'] if 'next' in links else None

        return response.json(), next_link

    def ticket_exists(self, id, target):
        """Determine whether an id is already in use for a ticket.

        Args:
            id (int): id to check
            target (string): db table to check

        Returns:
            int: 1 if the id is in use, 0 if it is not
        """
        sql_string = "SELECT COUNT(1) FROM " + target + " WHERE id = " + str(id)
        self.cursor.execute(sql_string)
        return self.cursor.fetchone()[0]

    def insert_ticket(self, new_ticket, target):
        """Add a new ticket to the database.

        Args:
            new_ticket (ticket): the ticket to be added
            target (string): db table to add ticket to

        Returns:
            bool: true if the insertion is successful, false otherwise
        """
        # first, determine whether this id is already in the db
        ticket_exists = self.ticket_exists(new_ticket.attributes['id'], target)

        if not ticket_exists:
            sql_string = new_ticket.insert_string().replace("TABLENAME", target)
            self.cursor.execute(sql_string, new_ticket.get_insert_fields())
            self.cnxn.commit()
        
        return not ticket_exists

    def update_ticket(self, new_ticket, target):
        """Update a ticket in the database.

        Args:
            new_ticket (ticket): the ticket to overwrite an existing ticket
            target (string): db table to update ticket in

        Returns:
            bool: true if the update is successful, false otherwise
        """
        ticket_exists = self.ticket_exists(new_ticket.attributes['id'], target)

        if ticket_exists:
            sql_string = new_ticket.update_string().replace("TABLENAME", target)
            self.cursor.execute(sql_string, new_ticket.get_update_fields())
            self.cnxn.commit()
        
        return bool(ticket_exists)

    def get_new_incidents(self):
        """Add all of the newest incidents to the database.
        """

        # get all the ids for tickets currently in the db
        self.cursor.execute("SELECT id FROM " + self.tables['ticket_info'] + ";") 
        ids = [row[0] for row in self.cursor]

        # start making API calls
        new_tickets = []

        payload = {'layout' : 'long'}
        url = "https://api.samanage.com/incidents.json"

        while url:
            page, next_url = self.get_page(url, payload = payload) # get the current page of tickets

            # determine whether any current tickets are already in the database
            not_in_db = [ticket(incident) for incident in page if incident['id'] not in ids]

            # add new tickets
            new_tickets += not_in_db

            # if all current tickets are new, we move on to the next page
            if len(page) == len(not_in_db):
                url = next_url
                time.sleep(2)
            else: # if at least one ticket repeats, we're done
                url = None

        for new_ticket in new_tickets:
            self.insert_ticket(new_ticket, self.tables['ticket_info'])
            self.new_tickets += 1

    def update_db(self):
        """Bring db up to date with Samanage by pulling in all new incident data.
        """
        # all possible states except closed
        ticket_states = ['assigned', 'on hold', 'pending research', 
                    'awaiting input', 'pending', 'pending validation',
                    'new', 'partially complete', 'resolved', 'awaiting approval']

        self.get_new_incidents()
        # update info on all tickets that are still open
        updated_ids = [] # store the id of every ticket that gets updated in this process
        for state in ticket_states:
            payload = {'state' : state, 'layout' : 'long'}
            url = "https://api.samanage.com/incidents.json"
            while url:
                page, url = self.get_page(url, payload = payload)
                for incident in page:
                    tick = ticket(incident)
                    updated_ids.append(tick.attributes['id'])

                    if not self.insert_ticket(tick, self.tables['ticket_info']):
                        self.update_ticket(tick, self.tables['ticket_info'])
                        self.updated_tickets += 1
                        
        # update info on all tickets that have since been closed

        # get ids of all not-closed tickets
        self.cursor.execute("SELECT id FROM " + self.tables['ticket_info'] + " WHERE status <> 'Closed';") 
        not_closed = [row[0] for row in self.cursor]

        # determine which not-closed tickets weren't updated
        needs_closing = [id for id in not_closed if id not in updated_ids]
        # to close these tickets, call and update individually
        for id in needs_closing:
            payload = {'layout' : 'long'}
            url = "https://api.samanage.com/incidents/" + str(id) + ".json"
            response = requests.get(url, headers = self.headers, params = payload)
            tick = ticket(response.json())
            self.update_ticket(tick, self.tables['ticket_info'])
            self.updated_tickets += 1

        logging.info("Database updated with " + str(self.new_tickets) + " tickets added and " + str(self.updated_tickets) + " tickets changed.")

    def get_ticket_info(self):
        """Retrieve all ticket information as a DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing all ticket info in database.
        """
        self.cursor.execute("SELECT * FROM " + self.tables['ticket_info'] + ";")
        rows = self.cursor.fetchall()

        col_ids = [col[0] for col in rows[0].cursor_description]
        cols = [[row.__getattribute__(id) for row in rows] for id in col_ids]
        d = dict(zip(col_ids, cols))
        df = pd.DataFrame(data = d)

        return df

    def execute_sql(self, sql_string, params = None):
        retry_flag = True
        retry_count = 0
        while retry_flag and retry_count < 5:
            try:
                # is this necessary?
                if params:
                    self.cursor.execute(sql_string, params)
                else:
                    self.cursor.execute(sql_string)
                retry_flag = False
            except:
                logging.info("Database connection lost, retrying in 5 seconds...")
                retry_count += 1
                time.sleep(5)

        if retry_count == 5:
            logging.error("Could not reconnect to database, aborting.")
            return

        self.cnxn.commit()


    def get_tickets_in_queue_by_assignee(self):
        """Log the in-queue tickets by assignee.
        """
        df = self.get_ticket_info()
        
        in_queue = df[(df['status'] != "Resolved") & (df['status'] != "Closed") & (df['status'] != "Partially Complete")].copy()
        in_queue_by_assignee = in_queue.groupby(['assignee']).count()['id']

        ts = datetime.today()

        for item in in_queue_by_assignee.items():
            # TODO P A R A M A T E R I Z E
            sql_string = ("""INSERT INTO TABLENAME (assignee, week, open_tickets) VALUES ('""" + \
                str(item[0]) + "', '" + str(ts) + "', '" + str(item[1]) + \
                 "');").replace("TABLENAME", self.tables['weekly_in_queue'])

            self.execute_sql(sql_string)

    def get_end_of_month_ticket_counts(self):
        """Log the number of in-queue, closed, and created tickets at the end of the month.
        """
        df = self.get_ticket_info()

        # determine previous month
        today = datetime.today()
        prev_month = 12 if today.month == 1 else today.month - 1
        prev_month_year = today.year - 1 if today.month == 1 else today.year
        prev_month_last_day = monthrange(prev_month_year, prev_month)[1]
        end_of_month = datetime(prev_month_year, prev_month, prev_month_last_day)

        # count tickets created in month
        created_in_month = df[[date.year == prev_month_year and date.month == prev_month for date in df['created_at']]].copy()
        created_in_month_count = int(created_in_month.count()['id'])
        created_in_month_by_department = created_in_month.groupby(['department']).count()['id']

        for item in created_in_month_by_department.items():
            sql_string = "INSERT INTO TABLENAME (department, date, created_tickets) VALUES (?, ?, ?);".replace("TABLENAME", self.tables['monthly_created'])
            self.execute_sql(sql_string, params = [str(item[0]), str(end_of_month), int(item[1])])

        # count tickets closed in month
        closed_in_month = df[[date is not None and date.year == prev_month_year and date.month == prev_month for date in df['to_resolve']]].copy()
        closed_in_month_count = int(closed_in_month.count()['id'])
        closed_in_month_by_assignee = closed_in_month.groupby(['assignee']).count()['id']

        for item in closed_in_month_by_assignee.items():
            sql_string = "INSERT INTO TABLENAME (assignee, date, closed_tickets) VALUES (?, ?, ?);".replace("TABLENAME", self.tables['monthly_closed'])
            self.execute_sql(sql_string, params = [str(item[0]), str(end_of_month), int(item[1])])

        # count tickets in queue at end of month
        in_queue = df[(df['status'] != "Resolved") & (df['status'] != "Closed") & (df['status'] != "Partially Complete")].copy()
        in_queue_count = int(in_queue.count()['id'])
        in_queue_by_assignee = in_queue.groupby(['assignee']).count()['id']

        for item in in_queue_by_assignee.items():
            sql_string = "INSERT INTO TABLENAME (assignee, date, open_tickets) VALUES (?, ?, ?);".replace("TABLENAME", self.tables['monthly_in_queue'])
            self.execute_sql(sql_string, params = [str(item[0]), str(end_of_month), int(item[1])])

        # add total counts to monthly_counts table  
        sql_string = "INSERT INTO TABLENAME (date, in_queue, created, closed) VALUES (?, ?, ?, ?);".replace("TABLENAME", self.tables['monthly_counts'])
        self.execute_sql(sql_string, params = [str(end_of_month), in_queue_count, created_in_month_count, closed_in_month_count])  

    def hard_reset(self):
        """Hard reset the database by pulling all data fresh from Samanage. Use only when absolutely necessary.
        """
        logging.info("Hard reset initiated at " + str(datetime.now()))
        # First, remove all existing records
        sql_string = "DELETE FROM " + self.tables['ticket_info'] + ";"
        self.cursor.execute(sql_string)

        # Next, start pulling pages
        url = "https://api.samanage.com/incidents.json"
        payload = {"layout" : "long"}

        page_count = 1

        while url:
            if self.debug:
                print("Getting page: " + str(page_count) + "...")
            page, url = self.get_page(url, payload = payload)

            for incident in page:
                tick = ticket(incident)
                retry_flag = True
                retry_count = 0
                while retry_flag and retry_count < 5:
                    try:
                        self.insert_ticket(tick, self.tables['ticket_info'])
                        retry_flag = False
                    except:
                        logging.info("Database connection lost, retrying in 5 seconds...")
                        retry_count += 1
                        time.sleep(5)

                if retry_count == 5:
                    logging.error("Could not reconnect to database, aborting hard reset.")
                    return

            page_count += 1

        logging.info("Hard reset completed at " + str(datetime.now()))

    def close_connection(self):
        """Close database connection.
        """
        self.cnxn.close()


class ticket:
    """Container for incident information.

    Attributes:
        attributes (dict): contains the important information designating each ticket
    """

    def __init__(self, input):
        self.attributes = {
            'id' : input['id'],
            'number' : input['number'],
            'name' : input['name'],
            'status' : input['state'],
            'priority' : input['priority'],
            'category' : input['category']['name'] if input['category'] is not None else None,
            'subcategory' : input['subcategory']['name'] if input['subcategory'] is not None else None,
            'assignee' : input['assignee']['name'] if input['assignee'] is not None else None,
            'requester' : input['requester']['name'] if input['requester'] is not None else None,
            'created_at' : input['created_at'],
            'updated_at' : input['updated_at'],
            'created_by' : input['created_by']['name'] if input['created_by'] is not None else None,
            'site' : input['site']['name'] if input['site'] is not None else None,
            'department' : input['department']['name'] if input['department'] is not None else None
        }

        target_stats = ["to_assignment", "to_first_response", "to_resolve", "to_close"]

        # a select few stats use UTC offset format instead of timezone name, so this handles those cases
        date_formats = ["%Y-%m-%d %H:%M:%S %Z", "%Y-%m-%d %H:%M:%S %z"]

        # special time stats processed seperately since dates need to be formatted
        for target in target_stats:
            for stat in input['statistics']:
                if stat['statistic_type'] == target:
                    for format in date_formats:
                        try:
                            dt = datetime.strptime(stat['value'], format)
                        except ValueError:
                            pass
                        
                    # microsecond and time zone information is appended manually since it's invariant
                    # and the datetime module's formatting doesn't match SQL Server's
                    self.attributes[target] = dt.strftime("%Y-%m-%dT%H:%M:%S") + ".000-07:00" if dt else None
                
                else:
                    self.attributes[target] = None
    
    def insert_string(self):
        """Parameterized SQL query string for inserting the ticket.

        Returns:
            string: the parameterized SQL query.
        """
        return "INSERT INTO TABLENAME" + \
            " (" + ", ".join(self.attributes.keys()) + ") " + \
            "VALUES (" + ", ".join("?" * len(self.attributes)) + ");"

    def get_insert_fields(self):
        """Returns ticket values in order to be inserted into parameterized SQL insert query.

        Returns:
            tuple: properly formatted ticket values.
        """
        return tuple(self.attributes.values())

    def update_string(self):
        """Parameterized SQL query string for updating the ticket.

        Returns:
            string: the parameterized SQL query.
        """
        return "UPDATE TABLENAME SET " + \
            ", ".join([key + " = ?" for key in self.attributes.keys() if key != 'id']) + \
            " WHERE id = " + str(self.attributes['id']) + ";"

    def get_update_fields(self):
        """Returns ticket values in order to be inserted into parameterized SQL update query.

        Returns:
            tuple: properly formatted ticket values.
        """
        return tuple([self.attributes[key] for key in self.attributes.keys() if key != 'id'])

    def __str__(self):
        return "TICKET: " + '; '.join([key + " : " + str(self.attributes[key]) for key in self.attributes])

def set_environment_vars():
    vals = {
        "db_name" : "",
        "db_password" : "",
        "db_server" : "",
        "db_username" : "",
        "X_Samanage_Authorization" : ""
    }
    for key in vals:
        os.environ[key] = vals[key]