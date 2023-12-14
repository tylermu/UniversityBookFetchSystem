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

    #function handles adding a new university ---------------------------------------------------------------------------------------------
def addUniversity(cursor, connection):
    response = input("\nDo you want to add a new university to the system (y/n)? ")
    if response.lower() != 'y':
        return

    print("\nThis is NOT a transaction. Please do not exit this process until complete..")
    print("")

    while True:
        universityName = input("Enter the name of the university you wish to add: ")
        if len(universityName) <= 100:
            break
        else:
            print("Invalid name length. Please enter a name with 100 characters or fewer.")

    #loop to ensure adminID is valid
    while True:
        adminID = input("Enter your admin ID: ")
        query = f"SELECT COUNT(*) FROM administrator WHERE admin_employeeID = {adminID}"
        cursor.execute(query)
        count = cursor.fetchone()[0]

        #if adminID exists, continue
        if count > 0:
            break
        else:
            print("Invalid ID. Please input a valid adminID")

    insert_query = """
    INSERT INTO university (university_name, admin_employeeID)
    VALUES (%s, %s)
    """
    cursor.execute(insert_query, (universityName, 1))
    connection.commit()

    
    query = f"SELECT universityID FROM university WHERE university_name = '{universityName}'"
    cursor.execute(query)
    universityID = cursor.fetchone()[0]

    print("Added university with the name: " + universityName)

    print("\nHere are the current departments")
    select_and_print(cursor, "SELECT departmentID, dep_name FROM department", "Displaying data from the 'department' table", ["departmentID", "dep_name"])
    response = input("\nDo you want to add a new department to the system (y/n)? ")
    if response.lower() == 'y':
        addDepartment(cursor, connection)

    print("\nHere are the current departments")
    select_and_print(cursor, "SELECT departmentID, dep_name FROM department", "Displaying data from the 'department' table", ["departmentID", "dep_name"])

    while True:
        print("Enter the departments you would like to associate to " + universityName)
        departments = input("Put them in a comma seperated list like '1,2,3' with NO spaces: ")
        if is_comma_separated_list(departments) is True:
            break
        else:
            print("Please put the departments in a comma seperated list with NO SPACES like: 1,2,3")

    departments_list = [(department) for department in departments.split(',')] #all the dept numbers in departments_list

    for each in departments_list:
        insert_query = """
        INSERT INTO university_department (universityID, departmentID)
        VALUES (%s, %s)
        """

        cursor.execute(insert_query, (universityID, each))
        connection.commit()
        while True:
            response = input("Would you like to add a course for dept with deptID " + each + " (y/n)?")
            if response == 'y':
                addCourse(cursor, connection, each)
            else:
                break

    while True:
        response = input("Would you like to associate books to a course (y/n)?")
        if response != 'y':
            break
        else:
            courseToBook(cursor, connection)

    print("Finalizing query..")
    print("Done adding university with the name: " + universityName)

    #add a new department
def addDepartment(cursor, connection):
    print("Here are the current departments:")
    select_and_print(cursor, "SELECT departmentID, dep_name FROM department", "Displaying data from the 'department' table", ["departmentID", "dep_name"])
    while True:
        new_department = input("Enter the name of the department you want to add: ")
        if len(new_department) < 100:
            break
        else:
            print("Please put the name of the department you want to add")
    while True:
        depID = input("Enter the departmentID for the department: ")
        if int(depID) > 1:
            break
        else:
            print("Please enter an integer for the departmentID")
    
    insert_query = """
    INSERT INTO department (departmentID, dep_name)
    VALUES (%s, %s)
    """
    cursor.execute(insert_query, (depID, new_department))
    connection.commit()

    print(new_department + " has been added")
    redo = input("Would you like to add another dept (y/n)?")
    if redo == 'y':
        addDepartment(cursor, connection)
    else: 
        return

def addCourse(cursor, connection, deptID):
    while True:
        courseName = input("Enter the name of the course: ")
        if len(courseName) < 100:
            break
        else:
            print("Please enter a valid course name with less than 100 characters")

    while True:
        courseID = input("Enter the ID for the course: ")
        if int(courseID) >= 1:
            break
        else:
            print("Please enter a valid courseID")

    #loop to ensure adminID is valid
    while True:
        adminID = input("Enter your admin ID: ")
        query = f"SELECT COUNT(*) FROM administrator WHERE admin_employeeID = {adminID}"
        cursor.execute(query)
        count = cursor.fetchone()[0]

        #if adminID exists, continue
        if count > 0:
            break
        else:
            print("Invalid ID. Please input a valid adminID")
    
    insert_query = """
    INSERT INTO course (courseID, course_name,  departmentID, admin_employeeID)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (courseID, courseName, deptID, adminID))
    connection.commit()

    print("Course added successfully")
    
    return

def courseToBook(cursor, connection):
    print("\nHere are the current books in the system")
    select_and_print(cursor, "SELECT isbn, book_title FROM book", "Displaying data from the 'book' table", ["isbn", "book title"])
    
    while True:
        bookISBN = input("\nEnter the isbn for the book you want to associate to a course:")
        if len(bookISBN) < 20:
            break
        else:
            print("Please input a valid ISBN")

    print("\nHere are the current courses in the system")
    select_and_print(cursor, "SELECT courseID, course_name FROM course", "Displaying data from the 'course' table", ["courseID", "course name"])

    while True:
        courseID2 = input("\nEnter the courseID for the course you want to associate to the book:")
        if len(courseID2) < 20:
            break
        else:
            print("Please input a valid courseID")

    insert_query = """
    INSERT INTO course_books (courseID, isbn)
    VALUES (%s, %s)
    """
    cursor.execute(insert_query, (courseID2, bookISBN))
    connection.commit()

    print("\nBook successfully connected to the course")

def updateInventory(cursor, connection):
    response = input("\nDo you want to update a books inventory number in the system (y/n)? ")
    if response.lower() != 'y':
        return
    print("\nThe books currently in the system are")
    select_and_print(cursor, "SELECT isbn, book_title FROM book", "Displaying data from the 'book' table", ["isbn", "book title"])

    # Loop to ensure ISBN exists in the book table
    while True:
        isbn = input("\nEnter the isbn for the book you wish to change the inventory number for: ")
        book_query = f"SELECT COUNT(*) FROM book WHERE isbn = '{isbn}'"
        cursor.execute(book_query)
        book_count = cursor.fetchone()[0]

        # If ISBN exists in book table, break the loop
        if book_count > 0:
            break
        else:
            print("ISBN does not exist in the book table. Please input a valid ISBN.")

    inventoryNum = f"SELECT inventory_number FROM book WHERE isbn = '{isbn}'"
    cursor.execute(inventoryNum)
    inventoryNum = cursor.fetchone()[0]

    print("\nThe book currently has " + str(inventoryNum) + " copies in stock")

    while True:
        newInventory = input("How many copies of this book should be in inventory? ")
        if int(newInventory) >= 0:
            query = """
                    UPDATE book
                    SET inventory_number = %s
                    WHERE isbn = %s
                    """
            cursor.execute(query, (newInventory, isbn))
            connection.commit()
            print("The book with the isbn " + isbn + " has a new inventory number of " + str(newInventory))
            break
        else: 
            print("Please enter the number of copies this book has (must be a number greater than 0)")
