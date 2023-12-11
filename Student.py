from sharedModule import connect_to_database, select_and_print
import re
from datetime import datetime

def studentmain(cursor, connection):

    print(f"\n======= Student Menu =======")
    
    while True:
    
        print("")
        print("Which action are you performing?")
        print("1. Create Student Account")
        print("2. Shop for Books")
        print("3. View Carts and Checkout")
        print("4. Submit Book Review")
        print("5. Create Trouble Ticket")
        print("6. Go Back")

        response = input("Enter number: ")
        if response == '1':
            addStudent(cursor, connection)
        elif response == '2':
            #User wants to shop for books
            shopBooks(cursor, connection)
        elif response == '3':
            #User wants to view their cart
            viewCart(cursor, connection)
        elif response == '4':
            #User wants to review a book they've purchased
            submitReview(cursor, connection)
        elif response == '5':
            #User wants to file a complaint via the trouble ticket system
            createTroubleTicket(cursor, connection)
        elif response == '6':
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
def shopBooks(cursor, connection):
    while True:
        
        # Prompt user for search term
        search_term = input("\nEnter your search term (title, author, category, subcategory, or keyword) or press Enter for all books: ")

        # Construct the SQL query based on the search term
        if search_term:
            query = f"""
            SELECT b.isbn, b.book_title, GROUP_CONCAT(a.author_name) AS authors, b.price, b.edition, b.format
            FROM book b
            LEFT JOIN author a ON b.isbn = a.isbn
            LEFT JOIN book_keyword k ON b.isbn = k.isbn
            WHERE b.book_title LIKE %s OR a.author_name LIKE %s OR b.category LIKE %s OR b.subcategory LIKE %s OR k.keyword_description LIKE %s
            GROUP BY b.isbn
            """
            params = (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
        else:
            query = """
            SELECT b.isbn, b.book_title, GROUP_CONCAT(a.author_name) AS authors, b.price, b.edition, b.format
            FROM book b
            LEFT JOIN author a ON b.isbn = a.isbn
            GROUP BY b.isbn
            """
            params = ()

        # Display books based on the search
        select_and_print(cursor, query, "Displaying search results", ["isbn", "book_title", "author", "price", "edition", "format"], params=params)
        
        #ask user if they want to add a book to their cart
        response = input("\nDo you want to add a book to cart (y/n)? ")
        if response.lower() != 'y':
            break

        #Ensures that the ISBN entered exists in the database
        isbn = input("Select the isbn of the book you wish to add to cart: ")
        query = f"SELECT COUNT(*) FROM book WHERE isbn = {isbn}"
        cursor.execute(query)
        count = cursor.fetchone()[0]

        #If book exists in database
        if count > 0:
                
            # Retrieve the price of the book for use later
            query = f"SELECT price FROM book WHERE isbn = {isbn}"
            cursor.execute(query)
            price = cursor.fetchone()[0]
            
            #loop to ensure purchase type is valid
            while True:
                purchaseType = input("Enter purchase type (rent/buy): ")
                if purchaseType.lower() in ['rent', 'buy']:
                    break
                else:
                    print("Invalid purchase type. Please enter 'rent' or 'buy'.")

            #loop to ensure quantity is valid
            while True:
                quantity = int(input("Enter quantity: "))
                if quantity > 0:
                    break
                else:
                    print("Invalid quantity. Please enter a quantity greater than 0")
            
            #loop to ensure studentID is valid
            while True:
                studentID = input("Enter your student ID: ")
                query = f"SELECT COUNT(*) FROM student WHERE studentID = {studentID}"
                cursor.execute(query)
                count = cursor.fetchone()[0]

                #if studentID exists, continue
                if count > 0:
                    #check if cart exists
                    query = f"SELECT cartID, total_cost FROM cart WHERE studentID = {studentID}"
                    cursor.execute(query)
                    cart_result = cursor.fetchall()

                    #if cart exists, continue
                    if cart_result:
                            #print list of carts for user to choose which one to add book to
                            select_and_print_cart_details(cursor, studentID)

                            while True:
                                cartID_input = input("Enter the cartID to add the book to: ")

                                # Check if the entered cartID is valid
                                if any(cartID_input == str(cart[0]) for cart in cart_result):
                                    cartID = int(cartID_input)
                                    total_cost = next(cart[1] for cart in cart_result if cart[0] == cartID)
                                    break
                                else:
                                    print("Invalid cartID. Please enter a valid cartID.")

                    else:
                        #create new cart
                        insert_query = """
                        INSERT INTO cart (total_cost, date_created, studentID)
                        VALUES (%s, %s, %s)
                        """   
                        #create empty cart
                        cursor.execute(insert_query, (0, datetime.now().date(), studentID))
                        connection.commit()

                        cartID = cursor.lastrowid
                        print(f"New cart created with cartID: {cartID}")
                        total_cost = 0

                    #record adding book to add_book table
                    insert_query = """
                    INSERT INTO add_book (isbn, cartID, quantity, purchase_type)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
                    """

                    cursor.execute(insert_query, (isbn, cartID, quantity, purchaseType))
                    connection.commit()
                    
                    #update total_cost and date_updated
                    total_cost += price * quantity
                    date_updated = datetime.now().date()

                    #record adding book to cart table
                    update_query = """
                    UPDATE cart
                    SET total_cost = %s, date_updated = %s
                    WHERE cartID = %s
                    """
                    cursor.execute(update_query, (total_cost, date_updated, cartID))
                    connection.commit()

                    print("Book successfully added to cart.")

                    break

                else:
                    print("\nInvalid student ID. Please enter a valid student ID")
            break

        #book does not exist in database, try again
        else:
            print("\nInvalid ISBN. Please enter a valid ISBN")

#handles displaying all carts and contents for a given student
def select_and_print_cart_details(cursor, studentID):
    query = """
    SELECT c.cartID, ab.quantity, b.book_title, b.isbn, b.price
    FROM cart c
    JOIN add_book ab ON c.cartID = ab.cartID
    JOIN book b ON ab.isbn = b.isbn
    WHERE c.studentID = %s
    """
    cursor.execute(query, (studentID,))
    result = cursor.fetchall()

    print("\n======= Cart Details =======")
    column_names = ["cartID", "quantity", "book_title", "isbn", "price"]
    if not result:
        print("No records found.")
    else:
        column_widths = [max(len(str(col)), max(len(str(row[i])) for row in result)) + 3 for i, col in enumerate(column_names)]
        print("  ".join(col.ljust(width) for col, width in zip(column_names, column_widths)))

        for row in result:
            print("  ".join(str(val).ljust(width) for val, width in zip(row, column_widths)))

def viewCart(cursor, connection):
    #Ensure valid studentID
    while True:
        studentID = input("Enter your student ID: ")
        query = f"SELECT COUNT(*) FROM student WHERE studentID = {studentID}"
        cursor.execute(query)
        count = cursor.fetchone()[0]

        #if studentID exists, continue
        if count > 0:
            #check if cart exists
            query = f"SELECT cartID, total_cost FROM cart WHERE studentID = {studentID}"
            cursor.execute(query)
            cart_result = cursor.fetchall()

            if cart_result:
                    #print list of carts for user to choose to interact with
                    select_and_print_cart_details(cursor, studentID)

                    while True:
                        continue_input = input("Do you want to view a cart in detail (y/n)? ")
                        if continue_input.lower() != 'y':
                            break

                        cartID_input = input("Enter the cartID of the cart to view in detail: ")

                        # Check if the entered cartID is valid
                        if any(cartID_input == str(cart[0]) for cart in cart_result):
                            cartID = int(cartID_input)
                            display_cart_contents(cursor, cartID)

                            while True:

                                print("Which action are you performing?")
                                print("1. Delete item from the cart")
                                print("2. Checkout")
                                print("3. Go Back")

                                response = input("Enter number: ")
                                if response == '1':
                                    deleted_item_isbn = input("Enter the isbn of the book you wish to delete from your cart: ")
                                    delete_book_from_cart(cursor, connection, cartID, deleted_item_isbn)
                                elif response == '2':
                                    submitOrder(cursor, connection, cartID)
                                elif response == '3':
                                    #User wants to exit
                                    break
                                else:
                                    print("\nInvalid choice, try again")

                                break
                        else:
                            print("Invalid cartID. Please enter a valid cartID.")
                        

            else:
                print("\nYou do not have any carts")
            
            break

        else:
            print("\nInvalid student ID. Please enter a valid student ID")

def display_cart_contents(cursor, cartID):
    query = """
    SELECT ab.quantity, b.book_title, b.isbn, b.price
    FROM add_book ab
    JOIN book b ON ab.isbn = b.isbn
    WHERE ab.cartID = %s
    """
    cursor.execute(query, (cartID,))
    result = cursor.fetchall()

    print("\n======= Cart Contents =======")
    column_names = ["quantity", "book_title", "isbn", "price"]
    if not result:
        print("The cart is empty.")
    else:
        column_widths = [max(len(str(col)), max(len(str(row[i])) for row in result)) + 3 for i, col in enumerate(column_names)]
        print("  ".join(col.ljust(width) for col, width in zip(column_names, column_widths)))

        for row in result:
            print("  ".join(str(val).ljust(width) for val, width in zip(row, column_widths)))

def delete_book_from_cart(cursor, connection, cartID, isbn):
    # Check if the ISBN exists in the cart
    query = "SELECT COUNT(*) FROM add_book WHERE cartID = %s AND isbn = %s"
    cursor.execute(query, (cartID, isbn))
    count = cursor.fetchone()[0]

    if count > 0:
        # Get the quantity and price of the book in the cart
        query = "SELECT quantity, price FROM add_book ab JOIN book b ON ab.isbn = b.isbn WHERE cartID = %s AND ab.isbn = %s"
        cursor.execute(query, (cartID, isbn))
        result = cursor.fetchone()
        quantity, book_price = result[0], result[1]

        # Delete the book from the cart
        delete_query = "DELETE FROM add_book WHERE cartID = %s AND isbn = %s"
        cursor.execute(delete_query, (cartID, isbn))
        connection.commit()

        # Update the total_cost in the cart
        update_query = "UPDATE cart SET total_cost = total_cost - %s WHERE cartID = %s"
        cursor.execute(update_query, (book_price * quantity, cartID))
        connection.commit()

        print("Book successfully deleted from the cart.")
    else:
        print("Invalid ISBN. The book does not exist in the cart.")

def submitOrder(cursor, connection, cartID):
    # Collect order information
    ship_type_options = ['standard', '2-day', '1-day']
    ship_type = input(f"Enter shipping type ({', '.join(ship_type_options)}): ").lower()
    while ship_type not in ship_type_options:
        print("Invalid shipping type. Please choose from the options.")
        ship_type = input(f"Enter shipping type ({', '.join(ship_type_options)}): ").lower()

    ship_address = input("Enter shipping address: ")

    # Collect credit card information
    credit_card_number = input("Enter credit card number: ")
    while not credit_card_number.isdigit() or len(credit_card_number) != 16:
        print("Invalid credit card number. Please enter a 16-digit number.")
        credit_card_number = input("Enter credit card number: ")

    credit_card_name = input("Enter credit card name: ")

    # Collect and validate credit card expiration date
    credit_card_expiration = input("Enter credit card expiration (YYYY-MM): ") + '-01'
    while not validate_date_format(credit_card_expiration, '%Y-%m-%d'):
        print("Invalid date format. Please enter the expiration date in YYYY-MM format.")
        credit_card_expiration = input("Enter credit card expiration (YYYY-MM): ")

    credit_card_type_options = ['VISA', 'MASTERCARD', 'AMERICAN EXPRESS', 'DISCOVER']
    credit_card_type = input(f"Enter credit card type ({', '.join(credit_card_type_options)}): ").upper()
    while credit_card_type not in credit_card_type_options:
        print("Invalid credit card type. Please choose from the options.")
        credit_card_type = input(f"Enter credit card type ({', '.join(credit_card_type_options)}): ").upper()

    # Insert credit card information into the credit_card table
    credit_card_insert_query = """
    INSERT INTO credit_card (credit_card_number, credit_card_name, credit_card_expiration, credit_card_type)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(credit_card_insert_query, (credit_card_number, credit_card_name, credit_card_expiration, credit_card_type))
    connection.commit()

    credit_cardID = cursor.lastrowid

    # Insert order information into the final_order table
    order_insert_query = """
    INSERT INTO final_order (cartID, date_created, status, ship_type, ship_address, credit_cardID)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(order_insert_query, (cartID, datetime.now().date(), 'new', ship_type, ship_address, credit_cardID))
    connection.commit()

    print("Order successfully submitted.")

def validate_date_format(date_string, date_format):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False

def submitReview(cursor, connection):
    return

def createTroubleTicket(cursor, connection):
    return
