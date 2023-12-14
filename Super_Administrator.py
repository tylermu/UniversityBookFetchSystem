from sharedModule import select_and_print, is_comma_separated_list

def superadministratormain(cursor, connection):
    print(f"\n======= Super Administrator Menu =======")
    
    while True:
    
        print("")
        print("Which action are you performing?")
        print("1. Add Customer Service Employee")
        print("2. Add Administrator Employee")
        print("3. Go Back")

        response = input("Enter number: ")
        if response == '1':
            addCustomerService(cursor, connection)
        elif response == '2':
            #User wants to shop for books
            addAdministrator(cursor, connection)
        elif response == '3':
            break
        else:
            print("\nInvalid choice, try again")

#add customer service employee
def addCustomerService(cursor, connection):
    response = input("\nDo you want to add a new customer service employee to the system (y/n)? ")
    if response.lower() != 'y':
        return
    while True:
        fname = input("\nEnter the first name of the new employee: ")
        if len(fname) <= 20:
            break
        else:
            print("Invalid name length. Please enter a name with 20 characters or fewer.")
    while True:
        lname = input("\nEnter the last name of the new employee: ")
        if len(lname) <= 30:
            break
        else:
            print("Invalid name length. Please enter a name with 30 characters or fewer.")

    insert_query = """
    INSERT INTO customer_support (cs_first_name, cs_last_name)
    VALUES (%s, %s)
    """
    cursor.execute(insert_query, (fname, lname))
    connection.commit()

    print("Customer support employee " + fname + " " + lname + " has been added to the system")

#add administrator
def addAdministrator(cursor, connection):
    response = input("\nDo you want to add a new administrator employee to the system (y/n)? ")
    if response.lower() != 'y':
        return
    while True:
        fname = input("\nEnter the first name of the new admin employee: ")
        if len(fname) <= 20:
            break
        else:
            print("Invalid name length. Please enter a name with 20 characters or fewer.")
    while True:
        lname = input("\nEnter the last name of the new admin employee: ")
        if len(lname) <= 30:
            break
        else:
            print("Invalid name length. Please enter a name with 30 characters or fewer.")

    insert_query = """
    INSERT INTO administrator (admin_first_name, admin_last_name)
    VALUES (%s, %s)
    """
    cursor.execute(insert_query, (fname, lname))
    connection.commit()

    print("Admin employee " + fname + " " + lname + " has been added to the system")
    
    