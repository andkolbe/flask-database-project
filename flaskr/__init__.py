# instead of creating a Flask instance globally, you will create it inside of a function 
# this function is known as the application factory
# any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned 

import os 
import mysql.connector
from mysql.connector import errorcode
from flask import Flask 

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

    cur.close()
    cnx.close()


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app  

def create_database(cursor):
    try:
        cursor.execute(
            'CREATE DATABASE {}'.format(DB_NAME))
    except mysql.connector.Error as err:
        print('Failed creating database: {}'.format(err))
        exit(1)