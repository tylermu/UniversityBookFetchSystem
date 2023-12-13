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


#function handles creating a ticket
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


    ##could probably delete this entire code chunk (while True and everything inside)
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
    #can replace above while True look with this code that gets the datestring:
    #dateLogged = datetime.now().date()

    #i know but i wanted to give the user to enter the date in case the problem occured earlier
    #than when the problem is entered. I just tell them to enter today's date because that will be
    #the most common date and will make it simpler for the user

    while True:
        ticketTitle = input("Please enter a title for your ticket. A title is required (Max = 100 characters): ")
        if 0 < len(ticketTitle) < 101:
            break
        else:
            print("Invalid title length. Please try again.")

    while True:
        problemDesc = input("Please describe the problem you are experiencing (Max = 500 characters): ")
        if len(problemDesc) <= 500:
            if len(problemDesc) == 0:
                problemDesc = None
            break
        else:
            print("Your description exceeds the limit of characters allowed. Please try again.")


    #we don't want hardcoded names. Instead prompt the user to enter their customer service ID, and use that in the query for cs_employeeID
    #however, check to ensure the entered cs_ID matches one in the database (see createTroubleTicket() method toward the bottom of Student.py)
    while True:
        csName = input("Please enter your first name all lowercase: ")
        if csName == "joan":
            csID = '1'
            break
        elif csName == "patricia":
            csID = '2'
            break
        elif csName == "julian":
            csID = '3'
            break
        elif csName == "dan":
            csID = '4'
            break
        elif csName == "kevin":
            csID = '5'
            break
        else:
            print("The name you entered is not recognized. Please try again.")

    status = 'new'



    insert_query = """
    INSERT INTO trouble_ticket (trouble_category, date_logged, ticket_title, prob_desc, cs_employeeID, status)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query, (troubleCategory, dateLogged, ticketTitle, problemDesc, csID, status))
    connection.commit()

    print("Touble ticket created successfully.")


#this function deletes a ticket given a ticketID
def deleteTicket(cursor,connection):

    while True:
        query = """
                SELECT *
                FROM trouble_ticket
                """
        select_and_print(cursor, query, "Displaying Trouble Tickets", ["ticketID", "trouble_category", "date_logged", "date_completed", "ticket_title", "prob_desc","fixed_desc","status","cs_employeeID","a_employeeID","studentID"])

        ticketID = input("Please enter the ticketID of the Trouble Ticket you would like to delete or enter nothing to escape.")

        if ticketID == "":
            return

        check_query = "SELECT * FROM trouble_ticket WHERE ticketID = %s"
        cursor.execute(check_query, (ticketID))
        result = cursor.fetchone()

        if result:
            sure = input("Are you sure you want to delete all Trouble Tickets where ticketID = " + ticketID + " (y/n)?")
            if sure == 'y':
                #if ticketID entered exists then it will delete those occurences
                delete_query = "DELETE FROM trouble_ticket WHERE ticketID = %s"
                cursor.execute(delete_query, (ticketID))
                connection.commit()
                print("Trouble Ticket successfully deleted.")
                break
        else:
            print("The ticketID you entered does not exist in the database.")



def updateTicket(cursor,connection):

    while True:
        while True:
            query = """
                    SELECT *
                    FROM trouble_ticket
                    """
            select_and_print(cursor, query, "Displaying Trouble Tickets", ["ticketID", "trouble_category", "date_logged", "date_completed", "ticket_title", "prob_desc","fixed_desc","status","cs_employeeID","a_employeeID","studentID"])

            ticketID = input("Please enter the ticketID of the Trouble Ticket you would like to update or enter nothing to escape.")

            if ticketID == "":
                return

            check_query = "SELECT * FROM trouble_ticket WHERE ticketID = %s"
            cursor.execute(check_query, (ticketID))
            result = cursor.fetchone()
            if result:
                break
            else:
                print("The ticketID you entered is not in the database.")


        if result:
            #need to make cases for adding assigned, in process and completed tuples
            while True:
                check_query = "SELECT * FROM trouble_ticket WHERE ticketID = %s AND status = 'in-process'"
                cursor.execute(check_query, (ticketID))
                result2 = cursor.fetchone()
                if result2:
                    print("You will be marking a Trouble Ticket as completed.")
                    while True:
                        dateCompleted = input("Please enter the date the Trouble Ticket was resolved in the format YYYY-MM-DD: ")
                        if(dateCompleted == ''):
                            leaveBlank =  input("Do you wish to not enter a date for your ticket (y/n)?")
                            if leaveBlank == 'y':
                                dateCompleted = None
                                break
                        if re.match('^\d{4}-\d{2}-\d{2}$', dateCompleted) is not None:
                            dateCompleted_obj = datetime.strptime(dateCompleted, '%Y-%m-%d')
                            if dateCompleted_obj > datetime(2023, 1, 1):
                                break
                            else:
                                print("The date you entered is invalid. Please try again.")
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
                    newTuple = list(result)
                    newTuple[3] = dateCompleted
                    newTuple[6] = fixDesc
                    newTuple[7] = 'completed'

                    insert_query = """
                    INSERT INTO trouble_ticket (ticketID, trouble_category, date_logged, date_completed, ticket_title, prob_desc,fixed_desc,status,cs_employeeID,a_employeeID,studentID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, tuple(newTuple))
                    connection.commit()

                    print("Touble ticket updated successfully.")
                    break
                check_query = "SELECT * FROM trouble_ticket WHERE ticketID = %s AND status = 'assigned'"
                cursor.execute(check_query, (ticketID))
                result3 = cursor.fetchone()
                if result3:
                    print("You are marking a Trouble Ticket as 'in-process'")
                    newTuple = list(result)
                    newTuple[7] = 'in-process'

                    insert_query = """
                    INSERT INTO trouble_ticket (ticketID, trouble_category, date_logged, date_completed, ticket_title, prob_desc,fixed_desc,status,cs_employeeID,a_employeeID,studentID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, tuple(newTuple))
                    connection.commit()

                    print("Touble ticket updated successfully.")
                    break
                check_query = "SELECT * FROM trouble_ticket WHERE ticketID = %s AND status = 'new'"
                cursor.execute(check_query, (ticketID))
                result4 = cursor.fetchone()
                if result4:
                    print("You will be marking a Trouble Ticket as 'assigned'")
                    while True:
                        aName = input("Please enter the first name of the administrator that you would liek to assign to the Touble Ticket in all lowercase: ")
                        if aName == "stephanie":
                            aID = '1'
                            break
                        elif aName == "peter":
                            aID = '2'
                            break
                        elif aName == "anthony":
                            aID = '3'
                            break
                        else:
                            print("The name you entered is not recognized. Please try again.")


                    newTuple = list(result)
                    newTuple[9] = aID
                    newTuple[7] = 'assigned'

                    insert_query = """
                    INSERT INTO trouble_ticket (ticketID, trouble_category, date_logged, date_completed, ticket_title, prob_desc,fixed_desc,status,cs_employeeID,a_employeeID,studentID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, tuple(newTuple))
                    connection.commit()

                    print("Touble ticket updated successfully.")
                    break


def deleteOrder(cursor,connection):

    while True:
        query = """
                SELECT *
                FROM final_order
                """
        select_and_print(cursor, query, "Displaying order information", ["orderID", "cartID", "date_created", "date_completed", "status", "shit_type", "ship_address", "credit_cardID" ])

        orderID = input("Please enter the orderID of the order that you would like to delete or enter nothing to escape.")

        if orderID == "":
            return



        check_query = "SELECT * FROM final_order WHERE orderID = %s"
        cursor.execute(check_query, (orderID))
        result = cursor.fetchone()
        
        if result:
            sure = input("Are you sure you want to delete the order where orderID = " + orderID + " (y/n)?")
            if sure == 'y':
                #if orderID entered exists then it will delete those occurences
                delete_query = "DELETE FROM final_order WHERE orderID = %s"
                cursor.execute(delete_query, (orderID))
                connection.commit()
                print("Order successfully deleted.")
                break
        else:
            print("The orderID you entered does not exist in the database.")


def updateOrder(cursor, connection):
    while True:
        query = """
                SELECT *
                FROM final_order
                """
        select_and_print(cursor, query, "Displaying order information", ["orderID", "cartID", "date_created", "date_completed", "status", "shit_type", "ship_address", "credit_cardID" ])

        orderID = input("Please enter the orderID of the order that you would like to update or enter nothing to escape.")

        if orderID == "":
            return


        check_query = "SELECT * FROM final_order WHERE orderID = %s"
        cursor.execute(check_query, (orderID))
        result = cursor.fetchone()
        
        if result:
            while True:
                print("Which attribute would you like to update?")
                print("1. Status")
                print("2. Ship type")
                print("3. Shipping address")
                attribute = input("Enter a number: ")
                
                if attribute == 1:
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
                    print("Order status successfully updated.")
                    yn = input("Would you like to update this order any further (y/n)?")
                    if yn == "n":
                        break
                
                elif attribute == 2:
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
                            statusString = "standard"
                            break
                        else:
                            print("The number you entered is invalid. Please try again.")
                    
                    update_query = "UPDATE final_order SET ship_type = %s WHERE orderID = %s"
                    cursor.execute(update_query, (statusString, orderID))
                    connection.commit()
                    print("Order ship type successfully updated.")
                    yn = input("Would you like to update this order any further (y/n)?")
                    if yn == "n":
                        break

                elif attribute == 3:
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
                    print("Order shipping address successfully updated.")
                    yn = input("Would you like to update this order any further (y/n)?")
                    if yn == "n":
                        break
                elif attribute == "":
                    break
                else:
                    print("The number you entered is invalid. Please try again or enter nothing to escape.")
                
        else:
            print("The orderID you entered is invalid. Please try again.")
        break













                    








                







        


