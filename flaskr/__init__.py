# instead of creating a Flask instance globally, you will create it inside of a function 
# this function is known as the application factory
# any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned 
import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request, jsonify
from flaskr.schema import TABLES 

DB_NAME = 'restaurantdb'

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3306
}

def create_app():
    # create and configure the app 
    # __name__ is the name of the current Python module
    # the app needs to know where it's located to set up some paths, and __name__ is a convenient way to tell it that 
    app = Flask(__name__)

    # connect to db
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)

    # create a cursor 
    cur = cnx.cursor()

    # use restaurantdb database
    try:
        cur.execute('USE {}'.format(DB_NAME))
    except mysql.connector.Error as err:
        print('Database {} does not exists.'.format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cur)
            print('Database {} created successfully.'.format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    # create tables 
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print('Creating table {}: '.format(table_name), end = '')
            cur.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('already exists')
            else:
                print(err.msg)
        else:
            print('OK')

    cur.close()
    cnx.close()


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.post('/employee')
    def employee_post():
        cnx = mysql.connector.connect(**config, database = DB_NAME)
        cursor = cnx.cursor()

        data = request.json

        if data is None: 
            return jsonify({'error': 'No JSON data provided'}), 400
        
        name = data.get('name')
        email = data.get('email')
        phoneNumber = data.get('phoneNumber')
        job = data.get('job')
        salary = data.get('salary')
        
        add_employee = ("""
            INSERT INTO employee
            (Name, Email, PhoneNumber, Job, Salary, RestaurantID)
            VALUES (%s, %s, %s, %s, %s, 1)
            """)
        
        cursor.execute(add_employee, (name, email, phoneNumber, job, salary))

        cnx.commit()

        cursor.close()
        cnx.close()

        return name

    return app  

def create_database(cursor):
    try:
        cursor.execute(
            'CREATE DATABASE {}'.format(DB_NAME))
    except mysql.connector.Error as err:
        print('Failed creating database: {}'.format(err))
        exit(1)