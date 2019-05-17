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
def home():
    db_admin()
    return render_template('index.html')

@app.route('/all_books')
def books():
    books = execute_sql('SELECT Category.description AS c_description, Book.description AS b_description, * FROM Category INNER JOIN Book ON Category.rowID=Book.category_id  ORDER BY c_description ASC')
    print(len(books))
    return render_template('all_books.html', books=books)

@app.route('/sql')
def sql():
    # sqlQ = execute_sql('DROP TABLE IF EXISTS Book',commit=True)
    # sqlQ = execute_sql('DROP TABLE IF EXISTS Category',commit=True)
    #
    # sqlQuery = execute_sql('CREATE TABLE Book (author TEXT,title TEXT, isbn INTEGER, description TEXT, category_id INTEGER)',commit=True)
    # sqlQuery = execute_sql('CREATE TABLE Category (description TEXT)',commit=True)

    sqlQuery2 = execute_sql('INSERT INTO Book (author,title,isbn, description, category_id) VALUES ("Mary Shelly","Frankenstein","1", "A horror story written by a romantic.","1")',commit=True)
    sqlQuery2 = execute_sql('INSERT INTO Book (author,title,isbn, description, category_id) VALUES ("Henry James","The Turn of the Screw","2", "Another British horror story.","1")',commit=True)
    sqlQuery2 = execute_sql('INSERT INTO Book (author,title,isbn, description, category_id) VALUES ("Max Weber","The Protestant Work Ethic and The Spirit of Capitalism","3", "A classic early 20th C. sociology text","2")',commit=True)
    sqlQuery2 = execute_sql('INSERT INTO Book (author,title,isbn, description, category_id) VALUES ("Robert Putnam","Bowling Alone","4", "A classic late 20th C. sociology test","2")',commit=True)
    sqlQuery2 = execute_sql('INSERT INTO Category (description) VALUES ("Horror")',commit=True)
    sqlQuery2 = execute_sql('INSERT INTO Category (description) VALUES ("Sociology")',commit=True)

    booksQuery = execute_sql('SELECT rowid, * FROM Book')
    for book in booksQuery:
        print(book['rowid'])
        print(book['author'])

    books = execute_sql('SELECT Category.description AS c_description, Book.description AS b_description, * FROM Category INNER JOIN Book ON Category.rowID=Book.category_id ')
    for book in books:
        print('ddd')
        print(book['c_description'])
        print(book['b_description'])
        print(book['title'])

    return '<h1>DB Seeded!</h1>'

@app.route('/erase_DB')
def eraseDB():
        # sqlQ = execute_sql('DROP TABLE IF EXISTS Book',commit=True)
        # sqlQ = execute_sql('DROP TABLE IF EXISTS Category',commit=True)
        sqlQ = execute_sql('DELETE FROM Book',commit=True)
        sqlQ = execute_sql('DELETE FROM Category',commit=True)
        return '<h1>DB Erased!</h1>'

def db_admin():
    sqlQuery = execute_sql('CREATE TABLE IF NOT EXISTS Book (author TEXT,title TEXT, isbn INTEGER, description TEXT, category_id INTEGER)',commit=True)
    sqlQuery = execute_sql('CREATE TABLE IF NOT EXISTS Category (description TEXT)',commit=True)


# @app.route('/employer/<employer_id>/review', methods={'GET','POST'})
# def review(employer_id):
#     if request.method == 'POST':
#         review = request.form['review']
#         rating = request.form['rating']
#         title = request.form['title']
#         status = request.form['status']
#
#         # to pass pluralsight qa the following line needs to be datetime.datetime.now().strftime("%m/%d/%Y")
#         # but to actually run the code without error it has to be datetime.now().strftime("%m/%d/%Y")
#         date = datetime.now().strftime("%m/%d/%Y")
#         returnStatus = execute_sql('INSERT INTO review (review, rating, title, date, status, employer_id) VALUES (?, ?, ?, ?, ?, ?)',
#         (review, rating, title, date, status, employer_id),commit=True)
#
#         return redirect(url_for('employer', employer_id=employer_id))
#
#     return render_template('review.html', employer_id=employer_id)
