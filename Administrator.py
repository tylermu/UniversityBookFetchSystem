from sharedModule import select_and_print, is_comma_separated_list

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
    
    print("")
    print("This is NOT a transaction. Please do not exit this process until complete..")
    print("")

    while True:
        universityName = input("Enter the name of the university you wish to add: ")
        if len(universityName) <= 100:
            break
        else:
            print("Invalid name length. Please enter a name with 100 characters or fewer.")

    insert_query = """
    INSERT INTO university (university_name)
    VALUES (%s)
    """
    cursor.execute(insert_query, (universityName))
    connection.commit()

    select_and_print(cursor, "SELECT departmentID, dep_name FROM department", "Displaying data from the 'department' table", ["departmentID", "dep_name"])

    response = input("\nDo you want to add a new department to the system (y/n)? ")
    if response.lower() == 'y':
        addDepartment(cursor, connection)

    while True:
        print("")
        print("Enter the departments you would like to associate to " + universityName)
        departments = input("Put them in a comma seperated list like '1,2,3': ")
        if is_comma_separated_list(departments) is True:
            break
        else:
            print("Please put the departments in a comma seperated list with NO SPACES like: 1,2,3")
    
    while True:
        print("")
        print("Enter the departments you would like to associate to " + universityName)
        departments = input("Put them in a comma seperated list like '1,2,3': ")
        if is_comma_separated_list(departments) is True:
            break
        else:
            print("Please put the departments in a comma seperated list with NO SPACES like: 1,2,3")

    departments_list = [(department) for department in departments.split(',')] #all the dept numbers in departments_list
    


    #insert_query = """
    #INSERT INTO university (university_name)
    #VALUES (%s)
    #"""

    #cursor.execute(insert_query, (universityName))
    #connection.commit()

    #print("Added university with the name: " + universityName)

def addDepartment(cursor, connection):
    print("Here are the departments currently in the system: ")
    select_and_print(cursor, "SELECT departmentID, dep_name FROM department", "Displaying data from the 'department' table", ["departmentID", "dep_name"])
    while True:
        new_department = input("Enter the name of the department you want to add: ")
        if len(new_department) < 100:
            break
        else:
            print("Please put the name of the department you want to add")
    while True:
        new_department = input("Enter the name of the department you want to add: ")
        if len(new_department) < 100:
            break
        else:
            print("Please put the name of the department you want to add")
    
    print("")