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
            password="", #Enter your password
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

    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:

                print("Welcome to the BookFetch Database System")

                while True:

                    print("")
                    print("1. Student")
                    print("2. Customer Service Employee")
                    print("3. Administrator")
                    print("4. Super Administrator")
                    print("5. Quit Program")

                    response = input("Which user would you like to enter the database as? ")
                    if response == '1':
                        userPermissions = 'Student'
                        studentmain(cursor)
                    elif response == '2':
                        userPermissions = 'Customer Service Employee'
                        customerservicemain()
                    elif response == '3':
                        userPermissions = 'Administrator'
                        administratormain()
                    elif response == '4':
                        userPermissions = 'Super Administrator'
                        superadministratormain()
                    elif response == '5':
                        break
                    else:
                        print("\nInvalid choice, try again")

            connection.commit()

    except Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()