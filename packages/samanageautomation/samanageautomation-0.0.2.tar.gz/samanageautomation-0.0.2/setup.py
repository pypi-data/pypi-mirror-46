import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="samanageautomation",
    version="0.0.2",
    author="Bryan D. Hayes",
    author_email="bhayes@portofsandiego.org",
    description="A class for managing a database of Samanage trouble ticket data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/portofsandiego/samanage-automation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests','pandas','pyodbc']
)
