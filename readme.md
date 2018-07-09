**URL Service Django Project**

_Developer: Daniil Kostyshak_

**About:** This is Service when you can post your custom url  and get short url for this address and 
get some modified text and stats from it.

**Requirements:** Python 3.6 should be installed on your PC

**Installation**
1) Open your terminal and setup 
new virtualenv with the following command 
(replace virtualenv_name to your custom value): `virtualenv -p python3.6 virtualenv_name`

2) Go to the virtualenv directory: `cd virtualenv_name`

3) Use the following command: `source bin/activate`

4) Clone project from the GitHub: `git clone https://github.com/Daniil-Kost/url_manager.git`

5) Go to the project directory: `cd url_manager`

6) Install requirements: `pip3 install -r requirements.txt`

7) Setup SQLite DataBase with following command: `python manage.py migrate`

8) Add project table to the DB. Run the following command: `python manage.py makemigrations`

9) Synchronize last changes in the DB:  `python manage.py migrate`

**Usage**

1) Run command `python manage.py runserver`
2) Go to the http://localhost:8000 on your browser