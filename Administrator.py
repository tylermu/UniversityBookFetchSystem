from Main import select_and_print

def administratormain(cursor, connection):
    print(f"\n======= Administrator Menu =======")
    
    while True:
    
        print("")
        print("Which action are you performing?")
        print("1. Add Book To The System")
        print("2. Add University")
        print("3. Update Book Inventory Number")
        print("4. Go Back")

        response = input("Enter number: ")
        if response == '1':
            addBook(cursor, connection)
        elif response == '2':
            #User wants to shop for books
            addUniversity(cursor, connection)
        elif response == '3':
            #User wants to view their cart
            updateInventory(cursor, connection)
        elif response == '4':
            break
        else:
            print("\nInvalid choice, try again")

#function handles adding a new book
def addBook(cursor, connection):
    response = input("\nDo you want to add a book to the sytem (y/n)? ")
    if response.lower() != 'y':
        return
    
    while True:
        bname = input("Enter the name of the book you would like to add: ")
        if len(bname) <= 200:
            break
        else:
            print("Invalid name length. Please enter a name with 200 characters or fewer.")


    while True:
        invNum = input("Enter the # of books in inventory for this title: ")
        if 1 < int(invNum):
            break
        else:
            print("Invalid inventory number. Please enter an inventory number greater than 1.")

    while True:
        isbn_num = input("Enter the ISBN # for this book: ")
        if 1 < int(isbn_num):
            break
        else:
            print("Invalid isbn number. Please enter an isbn number greater than 1.")

    insert_query = """
    INSERT INTO book (book_title, inventory_number, isbn)
    VALUES (%s, %s, %s)
    """

    cursor.execute(insert_query, (bname, invNum, isbn_num))
    connection.commit()

    print(bname + " added with an inventory number of : " + invNum)

    #function handles adding a new book
def addUniversity(cursor, connection):
    response = input("\nDo you want to add a new university to the system (y/n)? ")
    if response.lower() != 'y':
        return
    
    while True:
        universityName = input("Enter the name of the university you wish to add: ")
        if len(universityName) <= 100:
            break
        else:
            print("Invalid name length. Please enter a name with 100 characters or fewer.")

    select_and_print(cursor, "SELECT universityID, departmentID FROM university_department", "Displaying data from the 'university_department' table", ["universityID", "departmentID"])


    #insert_query = """
    #INSERT INTO university (university_name)
    #VALUES (%s)
    #"""

    #cursor.execute(insert_query, (universityName))
    #connection.commit()

    #print("Added university with the name: " + universityName)

