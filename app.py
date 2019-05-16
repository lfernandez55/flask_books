import sqlite3
from flask import Flask, render_template, g

PATH = 'db/books.sqlite'

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

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
    print('debugggg')
    return render_template('index.html')

@app.route('/sql')
def sql():
    sqlQ = execute_sql('DROP TABLE IF EXISTS Books')
    sqlQ = execute_sql('DROP TABLE IF EXISTS Category')

    sqlQuery = execute_sql('CREATE TABLE Books (author TEXT,title TEXT, isbn INTEGER, description DESCRIPTION, category_id INTEGER)')
    sqlQuery = execute_sql('CREATE TABLE Category (description TEXT)')
    print(sqlQuery)
    sqlQuery2 = execute_sql('INSERT INTO Books (author,title,isbn, description, category_id) VALUES ("Mary Shelly","Frankenstein","1", "A horror story written by a romantic.","1")')
    sqlQuery2 = execute_sql('INSERT INTO Books (author,title,isbn, description, category_id) VALUES ("Henry James","The Turn of the Screw","2", "Another British horror story.","1")')
    sqlQuery2 = execute_sql('INSERT INTO Books (author,title,isbn, description, category_id) VALUES ("Max Weber","The Protestant Work Ethic and The Spirit of Capitalism","3", "A classic early 20th C. sociology text","2")')
    sqlQuery2 = execute_sql('INSERT INTO Books (author,title,isbn, description, category_id) VALUES ("Robert Putnam","Bowling Alone","4", "A classic late 20th C. sociology test","2")')
    sqlQuery2 = execute_sql('INSERT INTO Category (description) VALUES ("Horror")')
    sqlQuery2 = execute_sql('INSERT INTO Category (description) VALUES ("Sociology")')

    sqlQ = execute_sql('PRAGMA table_info(Books)')
    print(sqlQ)
    print(sqlQuery2)
    books = execute_sql('SELECT rowid, * FROM Books')
    print(books)
    for book in books:
        print(book['rowid'])
        print(book['author'])
    return render_template('index.html')
