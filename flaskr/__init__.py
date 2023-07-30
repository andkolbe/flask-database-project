# instead of creating a Flask instance globally, you will create it inside of a function 
# this function is known as the application factory
# any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned 

import os 
from flask import Flask 

def create_app(test_config = None):
    # create and configure the app 
    # __name__ is the name of the current Python module
    # the app needs to know where it's located to set up some paths, and __name__ is a convenient way to tell it that 
    # instance_relative_config=True tells the app that configuration files are relative to the instance folder 
    # the instance folder is located outside the flaskr package and can hold local data that shouldn't be commited to version control
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev', # used by flask and extensions to keep data safe. Should be overwritten with a random value for deployment
        DATABASE = ''
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app  