from Main import connect_to_database, select_and_print

def studentmain(cursor):

    print("Student Menu")
    
    while True:
    
        print("")
        print("1. Shop for Books")
        print("2. View Cart")
        print("3. Submit Order")
        print("4. Submit Book Review")
        print("5. Create Trouble Ticket")
        print("6. Go Back")

        response = input("Select an action: ")
        if response == '1':
            #User wants to shop for books
            shopBooks(cursor)
        elif response == '2':
            #User wants to view their cart
            viewCart(cursor)
        elif response == '3':
            #User wants to checkout
            submitOrder(cursor)
        elif response == '4':
            #User wants to review a book they've purchased
            submitReview(cursor)
        elif response == '5':
            #User wants to file a complaint via the trouble ticket system
            createTroubleTicket(cursor)
        elif response == '6':
            break
        else:
            print("\nInvalid choice, try again")

#function handles listing books and adding them to a cart
def shopBooks(cursor):
    while True:
        #list all books before prompting user if they want to add one to cart
        select_and_print(cursor, "SELECT isbn, book_title FROM book", "Displaying data from the 'book' table", ["isbn", "book_title"])
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
            print("Adding book to cart...")
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
