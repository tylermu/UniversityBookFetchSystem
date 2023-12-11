from Main import connect_to_database, select_and_print
import re
from datetime import datetime

def customerservicemain(cursor, connection):

    print(f"\n======= Customer Service Menu =======")
    
    while True:
    
        print("")
        print("Which action are you performing?")
        print("1. Create Trouble Ticket")
        print("2. Delete Trouble Ticket")
        print("3. Update Trouble Ticket")
        print("4. Delete Order")
        print("5. Update Order Status")
        print("6. Go Back")

        response = input("Enter number: ")
        if response == '1':
            createTicket(cursor, connection)
        elif response == '2':
            #User wants to shop for books
            deleteTicket(cursor, connection)
        elif response == '3':
            #User wants to view their cart
            updateTicket(cursor, connection)
        elif response == '4':
            #User wants to review a book they've purchased
            deleteOrder(cursor, connection)
        elif response == '5':
            #User wants to file a complaint via the trouble ticket system
            updateOrder(cursor, connection)
        elif response == '6':
            break
        else:
            print("\nInvalid choice, try again")


#function handles adding a new student
def createTicket(cursor, connection):
    response = input("\nDo you want to create a Trouble Ticket (y/n)? ")
    if response.lower() != 'y':
        return
    
    while True:
        print("Which category does your trouble ticket fall under?")
        print("1. User Profile")
        print("2. Products")
        print("3. Cart")
        print("4. Orders")
        print("5. Others")
        categoryNumber = input("Enter number: ")
        if categoryNumber == 1:
            troubleCategory = "userprofile"
            break
        elif categoryNumber == 2:
            troubleCategory = "Products"
            break
        elif categoryNumber == 3:
            troubleCategory = "Cart"
            break
        elif categoryNumber == 4:
            troubleCategory = "Orders"
            break
        elif categoryNumber == 5:
            troubleCategory = "Others"
            break
        else:
            print("Invalid choice. Please enter a number 1 through 5.")


    while True:
        dateLogged = input("Please enter today's date in the format YYYY-MM-DD: ")
        if(dateLogged == ''):
            leaveBlank =  input("Do you wish to not enter a date for your ticket (y/n)?")
            if leaveBlank == 'y':
                dateLogged = None
                break
        if re.match('^\d{4}-\d{2}-\d{2}$', dateLogged) is not None:
            dateLogged_obj = datetime.strptime(dateLogged, '%Y-%m-%d')
            if dateLogged_obj > datetime(2023, 1, 1):
                break
            else:
                print("The date you entered is invalid. Please try again.")
        else:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    while True:
        ticketTitle = input("Please enter a title for your ticket. A title is required (Max = 100 characters): ")
        if 0 < len(ticketTitle) < 101:
            break
        else:
            print("Invalid title length. Please try again.")

    while True:
        problemDesc = input("Please describe the problem you are experiencing (Max = 500 characters): ")
        if len(problemDesc) < 500:
            if len(problemDesc) == 0:
                problemDesc = None
            break
        else:
            print("Your description exceeds the limit of characters allowed. Please try again.")

    
    while True:
        print("What is the status of your trouble ticket?")
        print("1. New")
        print("2. Assigned")
        print("3. In-process")
        print("4. Completed")
        categoryNumber = input("Enter number: ")
        if categoryNumber == 1:
            status = "new"
            break
        elif categoryNumber == 2:
            status = "assigned"
            break
        elif categoryNumber == 3:
            status = "in-process"
            break
        elif categoryNumber == 4:
            status = "completed"
            break
        else:
            print("Invalid choice. Please enter a number 1 through 4.")

    while True:
        csName = input("Please enter your first name all lowercase: ")
        if csName == "joan":
            csID = 1
            break
        elif csName == "patricia":
            csID = 2
            break
        elif csName == "julian":
            csID = 3
            break
        elif csName == "dan":
            csID = 4
            break
        elif csName == "kevin":
            csID = 5
            break
        else:
            print("The name you entered is not recognized. Please try again.")


    insert_query = """
    INSERT INTO trouble_ticket (trouble_category, date_logged, ticket_title, prob_desc, cs_employeeID)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query, (troubleCategory, dateLogged, ticketTitle, problemDesc, csID))
    connection.commit()

    print("Touble ticket created successfully.")


