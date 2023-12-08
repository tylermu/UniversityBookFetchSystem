# run this command in terminal: pip install mysql-connector-python
from Student import *
from Customer_Service import *
from Administrator import *
from Super_Administrator import *

import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tyler0625!", #Enter your password
            database="cisc450project"
        )
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        raise

def execute_query(cursor, query, values=None):
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
    except Error as e:
        print(f"Error executing query: {e}")
        raise

def select_and_print(cursor, query, section_name, column_names=None):
    execute_query(cursor, query)
    result = cursor.fetchall()

    print(f"\n======= {section_name} =======")
    
    if not result:
        print("No records found.")
        return

    if column_names:
        print("  ".join(map(str, column_names)))
    
    for row in result:
        print("  ".join(map(str, row)))

def main():
    response = 6
    print("")
    print("Welcome to the BookFetch Database System")
    print("1. Student")
    print("2. Customer Service Employee")
    print("3. Administrator")
    print("4. Super Administrator")
    while response != 1 or response != 2 or response != 3 or response != 4:
        response = input("Which user would you like to enter the database as? ")
        if response == 1:
            userPermissions = 'Student'
            studentmain()
        if response == 2:
            userPermissions = 'Customer Service Employee'
            customerservicemain()
        if response == 3:
            userPermissions = 'Administrator'
            administratormain()
        if response == 4:
            userPermissions = 'Super Administrator'
            superadministratormain()



if __name__ == "__main__":
    main()