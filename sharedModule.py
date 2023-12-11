import re
from password import password
import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password, #Enter your password
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

def select_and_print(cursor, query, section_name, column_names=None, params=None):
    if params is not None:
        execute_query(cursor, query, params)
    else:
        execute_query(cursor, query)

    result = cursor.fetchall()

    print(f"\n======= {section_name} =======")

    if not result:
        print("No records found.")
        return

    if column_names:
        column_widths = [max(len(str(col)), max(len(str(row[i])) for row in result)) + 3 for i, col in enumerate(column_names)]
        print("  ".join(col.ljust(width) for col, width in zip(column_names, column_widths)))

    for row in result:
        print("  ".join(str(val).ljust(width) for val, width in zip(row, column_widths)))

def is_comma_separated_list(s):
    pattern = re.compile(r'^\s*\d+(\s*,\s*\d+)*\s*$')
    return bool(pattern.match(s))