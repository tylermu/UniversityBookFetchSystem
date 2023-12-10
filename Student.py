from Main import connect_to_database, select_and_print
import re
from datetime import datetime

def studentmain(cursor, connection):

    print(f"\n======= Student Menu =======")
    
    while True:
    
        print("")
        print("1. Create Student Account")
        print("2. Shop for Books")
        print("3. View Cart")
        print("4. Submit Order")
        print("5. Submit Book Review")
        print("6. Create Trouble Ticket")
        print("7. Go Back")

        response = input("Select an action: ")
        if response == '1':
            addStudent(cursor, connection)
        elif response == '2':
            #User wants to shop for books
            shopBooks(cursor)
        elif response == '3':
            #User wants to view their cart
            viewCart(cursor)
        elif response == '4':
            #User wants to checkout
            submitOrder(cursor)
        elif response == '5':
            #User wants to review a book they've purchased
            submitReview(cursor)
        elif response == '6':
            #User wants to file a complaint via the trouble ticket system
            createTroubleTicket(cursor)
        elif response == '7':
            break
        else:
            print("\nInvalid choice, try again")

#function handles adding a new student
def addStudent(cursor, connection):
    response = input("\nDo you want to create a student account (y/n)? ")
    if response.lower() != 'y':
        return
    
    while True:
        fname = input("Enter first name: ")
        if len(fname) <= 25:
            break
        else:
            print("Invalid name length. Please enter a name with 25 characters or fewer.")

    while True:
        lname = input("Enter last name: ")
        if len(lname) <= 25:
            break
        else:
            print("Invalid name length. Please enter a name with 25 characters or fewer.")

    while True:
        email = input("Enter email: ")
        if len(email) <= 60:
            break
        else:
            print("Invalid email length. Please enter an email with 60 characters or fewer.")

    while True:
        address = input("Enter complete address: ")
        if len(address) <= 50:
            break
        else:
            print("Invalid address length. Please enter an address with 50 characters or fewer.")

    while True:
        phone = input("Enter 10 digit phone number (no dashes): ")
        if re.match('^[0-9]{10}$', phone) is not None:
            break
        else:
            print("Invalid phone number format. Please enter exactly 10 digits.")

    while True:
        birthdate = input("Enter birthdate (YYYY-MM-DD): ")
        if re.match('^\d{4}-\d{2}-\d{2}$', birthdate) is not None:
            birthdate_obj = datetime.strptime(birthdate, '%Y-%m-%d')
            if birthdate_obj > datetime(1960, 1, 1):
                break
            else:
                print("Invalid birthdate. Please enter birthdate after Jan 1, 1960.")
        else:
            print("Invalid birthdate format. Please enter birthdate in YYYY-MM-DD format.")

    while True:
        status = input("Enter student status (Grad/UnderGrad): ")
        if status.lower() in ['grad', 'undergrad']:
            break
        else:
            print("Invalid student status. Please enter 'Grad' or 'UnderGrad'.")

    while True:
        major = input("Enter major: ")
        if len(major) <= 20:
            break
        else:
            print("Invalid major length. Please enter a major with 20 characters or fewer.")

    uniID = int(input("Enter university ID: "))
    year = int(input("Enter year in university (1-4): "))

    insert_query = """
    INSERT INTO student (student_first_name, student_last_name, email, address, phone, birthdate, major, student_status, year, universityID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query, (fname, lname, email, address, phone, birthdate, major, status, year, uniID))
    connection.commit()

    print("Student added successfully.")

#function handles listing books and adding them to a cart
def shopBooks(cursor):
    while True:
        #list all books before prompting user if they want to add one to cart
        query = """
        SELECT b.isbn, b.book_title, GROUP_CONCAT(a.author_name) AS authors, b.price, b.edition, b.format
        FROM book b
        LEFT JOIN author a ON b.isbn = a.isbn
        GROUP BY b.isbn
        """
        select_and_print(cursor, query, "Displaying data from the 'book' table", ["isbn", "book_title", "author", "price", "edition", "format"])
        response = input("\nDo you want to add a book to cart (y/n)? ")
        if response.lower() != 'y':
            break
        isbn = input("Select the isbn of the book you wish to add to cart: ")

        #Ensures that the ISBN entered exists in the database
        query = f"SELECT COUNT(*) FROM book WHERE isbn = {isbn}"
        cursor.execute(query)
        count = cursor.fetchone()[0]

        if count > 0:
            #Adds book to cart
            
            while True:
                purchaseType = input("Enter purchase type (rent/buy): ")
                if purchaseType.lower() in ['rent', 'buy']:
                    break
                else:
                    print("Invalid purchase type. Please enter 'rent' or 'buy'.")
            
            while True:
                studentID = input("Enter your student ID: ")
                query = f"SELECT COUNT(*) FROM student WHERE studentID = {studentID}"
                cursor.execute(query)
                count = cursor.fetchone()[0]

                if count > 0:
                    #valid studentID and valid book, time to create cart if one does not exist
                    print("hello")
                    
                else:
                    print("\nInvalid student ID. Please enter a valid student ID")
            break
        else:
            print("\nInvalid ISBN. Please enter a valid ISBN")

def viewCart(cursor):
    return

def submitOrder(cursor):
    return

def submitReview(cursor):
    return

def createTroubleTicket(cursor):
    return
