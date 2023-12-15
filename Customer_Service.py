from sharedModule import select_and_print
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
        print("5. Update Order")
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


#function handles creating a ticket
def createTicket(cursor, connection):
    response = input("\nDo you want to create a Trouble Ticket (y/n)? ")
    if response.lower() != 'y':
        return
    
    while True:
        # Ensure valid csID
        csID = input("\nEnter your customer service ID: ")
        while csID.isdigit() != True:
            print("\nInvalid customer support ID. Please enter a valid customer service ID")
            csID = input("\nEnter your customer service ID: ")
        query = f"SELECT COUNT(*) FROM customer_support WHERE employeeID = {csID}"
        cursor.execute(query)
        count = cursor.fetchone()[0]

        # if csID exists, continue
        if count > 0:
        
            while True:
                print("Which category does your trouble ticket fall under?")
                print("1. User Profile")
                print("2. Products")
                print("3. Cart")
                print("4. Orders")
                print("5. Others")
                categoryNumber = input("Enter number: ")
                if categoryNumber == '1':
                    troubleCategory = "userprofile"
                    break
                elif categoryNumber == '2':
                    troubleCategory = "products"
                    break
                elif categoryNumber == '3':
                    troubleCategory = "cart"
                    break
                elif categoryNumber == '4':
                    troubleCategory = "orders"
                    break
                elif categoryNumber == '5':
                    troubleCategory = "others"
                    break
                else:
                    print("Invalid choice. Please enter a number 1 through 5.")


            dateLogged = datetime.now().date()

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

            insert_query = """
            INSERT INTO trouble_ticket (trouble_category, date_logged, ticket_title, prob_desc, status, cs_employeeID, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (troubleCategory, dateLogged, ticketTitle, problemDesc, 'new', csID, 'CS'))
            connection.commit()

            print("\nTrouble ticket created successfully.")
            break

        else:
            print("\nInvalid customer support ID. Please enter a valid customer service ID")


#this function deletes a ticket given a ticketID
def deleteTicket(cursor,connection):

    query = """
            SELECT 
                ticketID,
                trouble_category,
                date_logged,
                date_completed,
                CASE WHEN LENGTH(ticket_title) > 15 THEN CONCAT(LEFT(ticket_title, 15), '...') ELSE ticket_title END AS ticket_title,
                CASE WHEN LENGTH(prob_desc) > 15 THEN CONCAT(LEFT(prob_desc, 15), '...') ELSE prob_desc END AS prob_desc,
                CASE WHEN LENGTH(fixed_desc) > 15 THEN CONCAT(LEFT(fixed_desc, 15), '...') ELSE fixed_desc END AS fixed_desc,
                status,
                cs_employeeID,
                a_employeeID,
                studentID
            FROM trouble_ticket;
        """
    select_and_print(cursor, query, "Displaying Trouble Tickets", ["ID", "category", "logged", "completed", "title", "prob_desc","fix_desc","status","cs_ID","a_ID","s_ID"])

    while True:

        ticketID = input("\nPlease enter the ticketID of the Trouble Ticket you would like to delete or enter nothing to escape: ")

        if ticketID == "":
            return

        check_query = "SELECT * FROM trouble_ticket WHERE ticketID = %s"
        cursor.execute(check_query, (ticketID,))
        result = cursor.fetchall()

        if result:
            sure = input("Are you sure you want to delete all Trouble Tickets where ticketID = " + ticketID + " (y/n)? ")
            if sure == 'y':
                #if ticketID entered exists then it will delete those occurences
                delete_query = "DELETE FROM trouble_ticket WHERE ticketID = %s"
                cursor.execute(delete_query, (ticketID,))
                connection.commit()
                print("\nTrouble Ticket successfully deleted.")
                break
        else:
            print("\nThe ticketID you entered does not exist in the database.")



def updateTicket(cursor,connection):

        query = """
            SELECT 
                ticketID,
                trouble_category,
                date_logged,
                date_completed,
                CASE WHEN LENGTH(ticket_title) > 15 THEN CONCAT(LEFT(ticket_title, 15), '...') ELSE ticket_title END AS ticket_title,
                CASE WHEN LENGTH(prob_desc) > 15 THEN CONCAT(LEFT(prob_desc, 15), '...') ELSE prob_desc END AS prob_desc,
                CASE WHEN LENGTH(fixed_desc) > 15 THEN CONCAT(LEFT(fixed_desc, 15), '...') ELSE fixed_desc END AS fixed_desc,
                status,
                cs_employeeID,
                a_employeeID,
                studentID
            FROM trouble_ticket;
        """
        select_and_print(cursor, query, "Displaying Trouble Tickets", ["ID", "category", "logged", "completed", "title", "prob_desc","fix_desc","status","cs_ID","a_ID","s_ID"])
        
        while True:

            ticketID = input("\nPlease enter the ticketID of the Trouble Ticket you would like to update or enter nothing to escape: ")

            if ticketID == "":
                return

            check_query = "SELECT * FROM trouble_ticket WHERE ticketID = %s"
            cursor.execute(check_query, (ticketID,))
            result = cursor.fetchall()
            if result:
                break
            else:
                print("The ticketID you entered is not in the database.")


        if result:
            #need to make cases for adding assigned, in process and completed tuples and also seeing if the ticket is already complete
            while True:
                check_query = "SELECT * FROM trouble_ticket WHERE ticketID = %s AND status = 'completed'"
                cursor.execute(check_query, (ticketID,))
                result1 = cursor.fetchall()
                if result1:
                    print("\nThis Trouble Ticket has already been completed and cannot be altered further.")
                    break

                check_query = "SELECT * FROM trouble_ticket WHERE ticketID = %s AND status = 'in-process'"
                cursor.execute(check_query, (ticketID,))
                result2 = cursor.fetchall()
                if result2:
                    print("\nYou will be marking a Trouble Ticket as completed.")
                    yn = input("Are you sure you would like to assign Trouble Ticket with ID = " + ticketID + " as 'completed' (y/n)? ")
                    if yn != "y":
                        break
                    while True:
                        dateCompleted = input("Please enter the date the Trouble Ticket was resolved in the format YYYY-MM-DD: ")
                        if(dateCompleted == ''):
                            leaveBlank =  input("Do you wish to not enter a date for your ticket (y/n)?")
                            if leaveBlank == 'y':
                                dateCompleted = None
                                break
                        if re.match('^\d{4}-\d{2}-\d{2}$', dateCompleted) is not None:
                            try:
                                dateCompleted_obj = datetime.strptime(dateCompleted, '%Y-%m-%d')
                                if dateCompleted_obj > datetime(2023, 1, 1):
                                    break
                            except ValueError:
                                print("Invalid date: ", dateCompleted)
                        else:
                            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                    
                    while True:
                        fixDesc = input("Please describe how the Trouble was resolved (Max = 500 characters): ")
                        if len(fixDesc) <= 500:
                            if len(fixDesc) == 0:
                                fixDesc = None
                            break
                        else:
                            print("Your description exceeds the limit of characters allowed. Please try again.")

                    #update the attributes in necessary columns for new inserted tuple
                    tuple = list(result2)
                    trouble_category = tuple[0][1]
                    date_logged = tuple[0][2]
                    date_completed = dateCompleted 
                    ticket_title = tuple[0][4] 
                    prob_desc = tuple[0][5]
                    fixed_desc = fixDesc
                    status = 'completed'
                    cs_employeeID = tuple[0][8]
                    a_employeeID = tuple[0][9]
                    studentID = tuple[0][10]
                    created_by = tuple[0][11]

                    insert_query = """
                    INSERT INTO trouble_ticket (ticketID, trouble_category, date_logged, date_completed, ticket_title, prob_desc,fixed_desc,status,cs_employeeID,a_employeeID,studentID,created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (ticketID, trouble_category, date_logged, date_completed, ticket_title, prob_desc,fixed_desc,status,cs_employeeID,a_employeeID,studentID,created_by))
                    connection.commit()

                    print("\nTouble ticket updated successfully.")
                    break
                check_query = "SELECT * FROM trouble_ticket WHERE ticketID = %s AND status = 'assigned'"
                cursor.execute(check_query, (ticketID,))
                result3 = cursor.fetchall()
                if result3:
                    print("\nYou are marking a Trouble Ticket as 'in-process'")
                    yn = input("Are you sure you would like to assign Trouble Ticket with ID = " + ticketID + " as 'in-process' (y/n)? ")
                    if yn != "y":
                        break
                    tuple = list(result3)
                    trouble_category = tuple[0][1]
                    date_logged = tuple[0][2]
                    date_completed = tuple[0][3] 
                    ticket_title = tuple[0][4] 
                    prob_desc = tuple[0][5]
                    fixed_desc = tuple[0][6]
                    status = 'in-process'
                    cs_employeeID = tuple[0][8]
                    a_employeeID = tuple[0][9]
                    studentID = tuple[0][10]
                    created_by = tuple[0][11]


                    insert_query = """
                    INSERT INTO trouble_ticket (ticketID, trouble_category, date_logged, date_completed, ticket_title, prob_desc,fixed_desc,status,cs_employeeID,a_employeeID,studentID,created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (ticketID, trouble_category, date_logged, date_completed, ticket_title, prob_desc,fixed_desc,status,cs_employeeID,a_employeeID,studentID,created_by))
                    connection.commit()

                    print("\nTouble ticket updated successfully.")
                    break
                check_query = "SELECT * FROM trouble_ticket WHERE ticketID = %s AND status = 'new'"
                cursor.execute(check_query, (ticketID,))
                result4 = cursor.fetchall()
                if result4:
                    print("\nYou will be marking a Trouble Ticket as 'assigned'")
                    yn = input("Are you sure you would like to assign Trouble Ticket with ID = " + ticketID + " as 'assigned' (y/n)? ")
                    if yn != "y":
                        break
                    while True:
                        aID = input("Please enter the ID of the administrator you would like to assign to the Trouble Ticket: ")
                        while aID.isdigit() != True:
                            print("\nInvalid administrator ID. Please enter a valid administrator ID")
                            aID = input("\nEnter the administrator ID: ")
                        query = f"SELECT COUNT(*) FROM administrator WHERE admin_employeeID = {aID}"
                        cursor.execute(query)

                        count = cursor.fetchone()[0]
                        if count > 0:
                            break
                        else:
                            print("\nInvalid administrator ID. Please enter a valid administrator ID")

                    tuple = list(result4)

                    trouble_category = tuple[0][1]
                    date_logged = tuple[0][2]
                    date_completed = tuple[0][3] 
                    ticket_title = tuple[0][4] 
                    prob_desc = tuple[0][5]
                    fixed_desc = tuple[0][6]
                    status = 'assigned'
                    cs_employeeID = tuple[0][8]
                    a_employeeID = aID
                    studentID = tuple[0][10]
                    created_by = tuple[0][11]

                    insert_query = """
                    INSERT INTO trouble_ticket (ticketID, trouble_category, date_logged, date_completed, ticket_title, prob_desc,fixed_desc,status,cs_employeeID,a_employeeID,studentID,created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (ticketID, trouble_category, date_logged, date_completed, ticket_title, prob_desc,fixed_desc,status,cs_employeeID,a_employeeID,studentID,created_by))
                    connection.commit()

                    print("\nTrouble ticket updated successfully.")
                    break


def deleteOrder(cursor,connection):

    query = """
                SELECT *
                FROM final_order
                """
    select_and_print(cursor, query, "Displaying order information", ["orderID", "cartID", "date_created", "date_completed", "status", "shit_type", "ship_address", "credit_cardID" ])

    while True:

        orderID = input("\nPlease enter the orderID of the order that you would like to delete or enter nothing to escape: ")

        if orderID == "":
            return



        check_query = "SELECT * FROM final_order WHERE orderID = %s"
        cursor.execute(check_query, (orderID,))
        result = cursor.fetchone()
        
        if result:
            sure = input("Are you sure you want to delete the order where orderID = " + orderID + " (y/n)? ")
            if sure == 'y':
                #if orderID entered exists then it will delete those occurences
                delete_query = "DELETE FROM final_order WHERE orderID = %s"
                cursor.execute(delete_query, (orderID,))
                connection.commit()
                print("\nOrder successfully deleted.")
                break
        else:
            print("\nThe orderID you entered does not exist in the database.")


def updateOrder(cursor, connection):
    while True:
        query = """
                SELECT *
                FROM final_order
                """
        select_and_print(cursor, query, "Displaying order information", ["orderID", "cartID", "date_created", "date_completed", "status", "ship_type", "ship_address", "credit_cardID" ])

        orderID = input("\nPlease enter the orderID of the order that you would like to update or enter nothing to escape: ")

        if orderID == "":
            return


        check_query = "SELECT * FROM final_order WHERE orderID = %s"
        cursor.execute(check_query, (orderID,))
        result = cursor.fetchone()
        
        if result:
            while True:
                print("\nWhich attribute would you like to update?")
                print("1. Status")
                print("2. Ship type")
                print("3. Shipping address")
                print("4. Date completed")
                attribute = input("Enter a number: ")
                
                if attribute == '1':
                    print("You have chosen to update the status attribute in this order.")
                    print("Which status would you like to assign to the order?")
                    print("1. New")
                    print("2. Processed")
                    print("3. Shipping")
                    print("4. Shipped")
                    print("5. Canceled")

                    while True:
                        status = input("Enter a number: ")
                        if status == '1':
                            statusString = "new"
                            break
                        elif status == '2':
                            statusString = "processed"
                            break
                        elif status == '3':
                            statusString = "shipping"
                            break
                        elif status == '4':
                            statusString = "shipped"
                            break
                        elif status == '5':
                            statusString = "canceled"
                            break
                        else:
                            print("The number you entered is invalid. Please try again.")
                    
                    update_query = "UPDATE final_order SET status = %s WHERE orderID = %s"
                    cursor.execute(update_query, (statusString, orderID))
                    connection.commit()
                    print("\nOrder status successfully updated.")
                    yn = input("\nWould you like to update this order any further (y/n)? ")
                    if yn == "n":
                        break
                
                elif attribute == '2':
                    print("You have chosen to update the ship type attribute in this order.")
                    print("Which ship type would you like to assign to the order?")
                    print("1. 1-day")
                    print("2. 2-day")
                    print("3. standard")

                    while True:
                        ship = input("Enter a number: ")
                        if ship == '1':
                            shipString = "1-day"
                            break
                        elif ship == '2':
                            shipString = "2-day"
                            break
                        elif ship == '3':
                            shipString = "standard"
                            break
                        else:
                            print("The number you entered is invalid. Please try again.")
                    
                    update_query = "UPDATE final_order SET ship_type = %s WHERE orderID = %s"
                    cursor.execute(update_query, (shipString, orderID))
                    connection.commit()
                    print("\nOrder ship type successfully updated.")
                    yn = input("\nWould you like to update this order any further (y/n)? ")
                    if yn == "n":
                        break

                elif attribute == '3':
                    print("You have chosen to update the ship address attribute in this order.")
                    while True:
                        address = input("Please enter the shipping address you would like to have assigned for this order (Max = 100 characters): ")
                        if len(address) > 100:
                            print("The address you entered is too long. Please try typing it another way.")
                        else:
                            break
                    update_query = "UPDATE final_order SET ship_address = %s WHERE orderID = %s"
                    cursor.execute(update_query, (address, orderID))
                    connection.commit()
                    print("\nOrder shipping address successfully updated.")
                    yn = input("\nWould you like to update this order any further (y/n)? ")
                    if yn == "n":
                        break

                elif attribute == "4":
                    print("You have chosen to update the date this order was completed.")
                    while True:
                        dateCompleted = input("Please enter the date the Trouble Ticket was resolved in the format YYYY-MM-DD: ")
                        if re.match('^\d{4}-\d{2}-\d{2}$', dateCompleted) is not None:
                            try:
                                dateCompleted_obj = datetime.strptime(dateCompleted, '%Y-%m-%d')
                                if dateCompleted_obj > datetime(2023, 1, 1):
                                    break
                            except ValueError:
                                print("Invalid date: ", dateCompleted)
                        else:
                            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                    update_query = "UPDATE final_order SET date_completed = %s WHERE orderID = %s"
                    cursor.execute(update_query, (dateCompleted, orderID))
                    connection.commit()
                    print("\nOrder completion date successfully updated.")
                    yn = input("\nWould you like to update this order any further (y/n)? ")
                    if yn == "n":
                        break

                elif attribute == "":
                    break
                else:
                    print("The number you entered is invalid. Please try again or enter nothing to escape.")
                
        else:
            print("The orderID you entered is invalid. Please try again.")
        break
