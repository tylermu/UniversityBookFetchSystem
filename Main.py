# run this command in terminal: pip install mysql-connector-python

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

                # Select from plane
                select_and_print(cursor, "SELECT book_title FROM book", "Displaying data from the 'book' table", ["book_title"])

                '''# Select from passengers with a join
                select_and_print(cursor, "SELECT p.f_name, p.l_name FROM passengers as p INNER JOIN onboard o ON p.ssn = o.ssn WHERE o.seat = '30C'", "Displaying passengers with seat '30C'", ["f_name", "l_name"])

                # Delete from plane
                execute_query(cursor, "DELETE FROM plane WHERE mph = 610")
                select_and_print(cursor, "SELECT * FROM plane", "Deleting planes with mph = 610", ["tail_no", "make", "model", "capacity", "mph"])

                # Insert into plane
                insert_query = "INSERT INTO plane VALUES (%s, %s, %s, %s, %s)"
                values = (3, 'McDonnel Douglas', 'DC10', 380, 610)
                execute_query(cursor, insert_query, values)
                select_and_print(cursor, "SELECT * FROM plane", "Inserting a new plane", ["tail_no", "make", "model", "capacity", "mph"])

                # Insert into flight
                flight_queries = [
                    "INSERT INTO flight VALUES (1, 'Springfield, IL', '7:15', 'Chicago, IL', '7:45', 3)",
                    "INSERT INTO flight VALUES (2, 'Columbus, OH', '16:00', 'Portland, OR', '22:00', 3)"
                ]
                for query in flight_queries:
                    execute_query(cursor, query)
                print("\n======= Inserting new flights and onboard records =======")

                # Update passengers
                update_query = "UPDATE passengers SET m_name = %s WHERE f_name = %s"
                update_values = ('L', 'Frank')
                execute_query(cursor, update_query, update_values)
                select_and_print(cursor, "SELECT * FROM passengers", "Updating passengers: Set middle name to 'L' for 'Frank'", ["ssn", "f_name", "l_name", "m_name"])'''

            connection.commit()

    except Error as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
