# run this command in terminal: pip install mysql-connector-python
from Student import *
from Customer_Service import *
from Administrator import *
from Super_Administrator import *
from sharedModule import *


def main():

    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:

                print("Welcome to the BookFetch Database System")

                while True:

                    print("")
                    print("Which user would you like to enter the database as?")
                    print("1. Student")
                    print("2. Customer Service Employee")
                    print("3. Administrator")
                    print("4. Super Administrator")
                    print("5. Quit Program")
                    response = input("Enter number: ")

                    if response == '1':
                        studentmain(cursor, connection)
                    elif response == '2':
                        customerservicemain(cursor, connection)
                    elif response == '3':
                        administratormain(cursor, connection)
                    elif response == '4':
                        superadministratormain(cursor, connection)
                    elif response == '5':
                        break
                    else:
                        print("\nInvalid choice, try again")

            connection.close()

    except Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()