from flask import Flask 

# create an instance of the Flask class
# __name__ is a shortcut for the name of the app's module or package
# this is needed so that Flask knows where to look for resources such as templates and static files 
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'