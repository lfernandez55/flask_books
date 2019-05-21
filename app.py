import sqlite3
from flask import Flask, render_template, g, request, redirect, url_for, jsonify
from pprint import pprint
from flask_bootstrap import Bootstrap

PATH = 'db/books.sqlite'

app = Flask(__name__)

bootstrap = Bootstrap( app)

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

@app.route('/seedDB')
def seedDB():
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


@app.route('/addbook', methods={'GET','POST'})
def addbook():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        isbn = request.form['isbn']
        description = request.form['description']
        category_field = request.form['category']

        categoryID = execute_sql('SELECT rowid, * FROM Category WHERE description = ? ',[category_field])
        if len(categoryID) == 0:
            returnStatus = execute_sql('INSERT INTO Category (description) VALUES (?)',[category_field],commit=True)
            returnQuery = execute_sql('SELECT last_insert_rowid()')
            categoryID = returnQuery[0][0]
            # or, instead of above two lines use this one instead:
            # categoryID = execute_sql('SELECT rowid, * FROM Category WHERE description = ? ',[category_field])
        else:
            categoryID = categoryID[0]['rowid']

        returnStatus = execute_sql('INSERT INTO Book (author, title, isbn, description, category_id) VALUES (?, ?, ?, ?, ?)',
        (author, title, isbn, description, categoryID),commit=True)

        return redirect(url_for('home'))

    categories = execute_sql('SELECT * FROM Category ORDER BY description ASC')
    return render_template('addbook.html', categories=categories)

@app.route('/categories')
def categories():
    categories = execute_sql('SELECT rowid, * FROM Category ORDER BY description ASC')
    return render_template('categories.html', categories=categories)

@app.route('/books_in_category/<categoryID>')
def books_in_cat(categoryID):
    categories = execute_sql('SELECT * FROM Category WHERE rowid = ? ',[categoryID])
    categoryDescription= categories[0]['description']
    books = execute_sql('SELECT * FROM Book WHERE category_id = ? ',[categoryID])
    for book in books:
        print('dddd')
    print('debug')
    return render_template('books_in_cat.html', books=books, categoryDescription=categoryDescription)

@app.route('/sql', methods={'GET','POST'})
def sql():
    data=""
    if request.method == 'POST':
        sqlField = request.form['sqlField']
        try:
            returnVar = execute_sql(sqlField)
        except:
            data="An error occurred. . .look in the console"
        else:
            try:
                for row in returnVar:
                    print('')
                    print(type(row))
                    rowAsDict = dict(row)
                    print(type(rowAsDict))
                    data = data + "\n"
                    for key, value in rowAsDict.items():
                        print(key, ":", value)
                        data= data + key + ":" + str(value) + "\n"
            except:
                 data="Data returned from sql was not iterable"
        return render_template('sql.html',data=data)

    return render_template('sql.html',data=data)



@app.route('/tinker')
def tinker():
    #iterating through a list of dictionaries (equivalent in js to iterating through an array of objects)
    mylist = [{'fname':'Luke','lname':'Fernandez'},{'fname':'Susan','lname':'Matt'}]
    print('=============================================')
    for item in mylist:
        print('')
        print(item)
        print(type(item))
        for key, value in item.items():
            print(key, ":", value)

    #iterating thru list.  with each item in list convert to dictionary and then iterate through the dictionary
    print('++++++++++++++++++++++++++++++++++++++++++++++')
    books = execute_sql('SELECT rowid, * FROM Book')
    for row in books:
        print('')
        print(type(row))
        rowAsDict = dict(row)
        print(type(rowAsDict))
        for key, value in rowAsDict.items():
            print(key, ":", value)

    return '<h1>Tinker function executed, check console</h1>'

@app.route('/tinker_extends')
def tinker_extends():
    return render_template('tinker_extends.html')

@app.route('/tinker_json')
def bar():
    # see https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
    tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
    ]
    return jsonify({'tasks': tasks})
