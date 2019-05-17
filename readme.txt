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
