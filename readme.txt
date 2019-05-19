1)python -m venv venv  (this installs the venv folder)
2)venv\Scripts\activate.bat
3)pip install Flask
4)add basic app.py file

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello, World!'

4.5) set FLASK_ENV=development  (so that server doesn't need to be restarted after every change)
5)flask run
(open browser on 5000 -- to use a different port use "flask run --port 8080")

-----------
ADDING A TEMPLATE
6)Add templates folder
7)Add index.html in folder
8)Modify app.py

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def books():
    return render_template('index.html')

-----------------
SETTING UP SQLITE
9) Add a folder called db
10) Modify app.py

import sqlite3
from flask import Flask, render_template, g

PATH = 'db/books.sqlite'

app = Flask(__name__)

def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection

def execute_sql(sql,values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql,values)
    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results

@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()


@app.route('/')
def books():
    jobs = execute_sql('')
    return render_template('index.html')

This creates the db/books.sqlite db (look in the directory structure)

-------------
ADD SOME TABLES

Decorators
https://www.python-course.eu/python3_decorators.php

jinja2 stuff in all_books.html
  conditionals
  length of a list
  setting variables
  setting variables inside loops
  https://stackoverflow.com/questions/9486393/jinja2-change-the-value-of-a-variable-inside-a-loop

--------------
addbook.html
request, redirect, url_for

---------------
Categories
Book_in_cat  (first use of parameter in url route)
SQL  (allows dynamic creation of SQL, also shows how query can be dumped by turning
each row into a dictionary and then iterating through the dictionary)

---------------
SQLLite3
Download from https://www.sqlite.org/download.html
Extract sqlite3.exe from zip
Copy db (books.sqllite) and place in same directory as exe
C:\Users\lfernandez\Downloads\junk\sqlite-tools-win32-x86-3280000>sqlite3 books.sqlite
run sql commands like:
sqlite> select * from category;
Horror
Sociology
sqlite> select * from book;
Mary Shelly|Frankenstein|1|A horror story written by a romantic.|1
Henry James|The Turn of the Screw|2|Another British horror story.|1
Max Weber|The Protestant Work Ethic and The Spirit of Capitalism|3|A classic early 20th C. sociology text|2
Robert Putnam|Bowling Alone|4|A classic late 20th C. sociology test|2
sqlite>
