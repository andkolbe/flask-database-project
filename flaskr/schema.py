import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'restaurants'

TABLES = {}
TABLES['restaurant'] = (
"""
    CREATE TABLE restaurant (
        ID INT NOT NULL,
        Name VARCHAR(45) NOT NULL,
        Address VARCHAR(125) NOT NULL,
        PhoneNumber VARCHAR(15) NOT NULL
        PRIMARY KEY (ID)
    )
"""
)

TABLES['employee'] = (
""" 
    CREATE TABLES employee (
        ID INT NOT NULL,
        Name VARCHAR(200) NOT NULL,
        Email VARCHAR(200) NOT NULL,
        PhoneNumber VARCHAR(15) NOT NULL,
        Job VARCHAR(50) NOT NULL,
        Salary INT NOT NULL,
        RestaurantID INT NOT NULL,
        PRIMARY KEY (ID),
        FOREIGN KEY (RestaurantID) REFERENCES restaurant(ID)
    )
"""
)

TABLES['menu'] = (
"""
    CREATE TABLE menu (
        ID INT NOT NULL,
        Name VARCHAR(45) NOT NULL,
        RestaurantID INT NOT NULL,
        PRIMARY KEY (ID),
        FOREIGN KEY (RestaurantID) REFERENCES restaurant(ID)
    )
"""
)

TABLES['dish'] = (
""" 
    CREATE TABLE dish (
        ID INT NOT NULL,
        Name VARCHAR(45) NOT NULL,
        Category VARCHAR(100) NOT NULL,
        Price DECIMAL NOT NULL,
        MenuID INT,
        PRIMARY KEY (ID),
        FOREIGN KEY (MenuID) REFERENCES menu(ID)
    )
"""
)