**URL Service Django Project**

_Developer: Daniil Kostyshak_

**About:** This is Service when you can post your custom url  and get short url for this address and 
get some modified text and stats from it.

**Requirements:** Python 3.6 should be installed on your PC

**Installation**
1) Clone project from the GitHub: `git clone https://github.com/Daniil-Kost/url_manager.git`

2) Go to the project directory: `cd url_manager`

3) Setup new virtualenv with the following command: `virtualenv -p python3.7 venv`

4) Activate env with the following command: `source venv/bin/activate`

5) Install requirements: `pip3 install -r requirements.txt`

6) Setup SQLite DataBase with following command: `python manage.py migrate`

7) Add project table to the DB. Run the following command: `python manage.py makemigrations`

8) Synchronize last changes in the DB:  `python manage.py migrate`

**Usage**

1) Run command `python manage.py runserver`
2) Go to the http://localhost:8000 on your browser

**Tests**

1) For run tests execute `python manage.py test`