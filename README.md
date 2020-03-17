# py-rda-reports
Create reports from Oracle RDA collections. 

## Supported profiles
OFM.WebLogicServer

## Output format
HTML, JSON

## Requirements
Python 3, pip, venv (virtualenv)

Python 3 for Windows includes pip and venv. For Linux, check specific instructions for your distribution on installing pip and venv.

## Virtualenv setup and dependencies downloads
Choose your working directory, and create a virtual env structure. 

For these examples, we will assume you cd'ed to current py-rda-reports app folder.

1. Create virtual environment

        python -m venv env
    
2. switch to app environment

    (on linux)

        source env/bin/activate

    (on windows)

        env\Scripts\activate

3. Fetch dependencies

        pip install -r requirements.txt

## Usage

We assume "env" virtual enviromnent folder is located directly under app folder.

1. Switch to project environment

    (on linux)

        source env/bin/activate

    (on windows)

        env\Scripts\activate

2. Configure RDA sources and output path

    + edit config.py

        ```
        COLLECTIONS = (
            {
                'machine-name': 'MACHINE1', 
                'context': 'SOA Domain A', 
                'path': '/path/to/rda/collections/RDA_SOADOM1/collect'
            },
            {
                'machine-name': 'MACHINE2', 
                'context': 'SOA Domain B', 
                'path': '/path/to/rda/collections/RDA_SOADOM2/collect'
            },
        )
        OUTPUT_PATH = '/put/absolute/path/here'
        ```

3. Run process

    + cd to app folder
    + execute

        (on linux )

            python ./rda_utils/start.py

        (on windows)

            python .\rda_utils\start.py
    + you should get something like:

        ```
        Processing  MACHINE1 SOA Domain A
            Domain-01 OK
            Domain-02 OK
        Processing  MACHINE2 SOA Domain B
            Domain-03 OK
            Domain-04 OK
        Successful outputs saved at C:\RDA-REPORTS
        ```
