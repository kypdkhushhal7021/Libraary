from flask import Flask, render_template, request, session, url_for, redirect, jsonify, make_response, flash
import sqlite3
import datetime
import random
import requests
app = Flask(__name__)

#########################################################################################################################################
#                                                  API random Selection
#########################################################################################################################################



FRAPPE_API_BASE_URL = "https://frappe.io/api/method/frappe-library"
def generate_random_page():
    return random.randint(1, 10)

def generate_api_url():
    page = generate_random_page()
    return f"{FRAPPE_API_BASE_URL}?page={page}&title=and"

# Example usage
for i in range(10):  # Run for 5 iterations
    api_url = generate_api_url()


#########################################################################################################################################
#                                                  Login Page
#########################################################################################################################################


@app.route('/',methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == "POST":
        session.pop('user', None)
        mailid = request.form.get("email")
        password = request.form.get("Pas")
        print(mailid, password)
        con = dbConnection()
        cursor = con.cursor()

        # Execute the query with proper placeholders
        cursor.execute('SELECT * FROM userdetails WHERE email = ? AND password = ?', (mailid, password))
        result = cursor.fetchone()

        if result:
            print("Login successful")
            session['userid'] = result[0]
            session['user'] = mailid
            return redirect(url_for('dashboard'))
        else:
            print("Login failed")
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)

    return render_template('login.html')


#########################################################################################################################################
#                                                   User Registeration
#########################################################################################################################################



@app.route('/register', methods=["GET", "POST"])
def register():
    
    return render_template('register.html')
    return render_template("login.html")



#########################################################################################################################################
#                                               Main initial page/dashboard
#########################################################################################################################################
def get_books_count():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM books')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_members_count():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM members')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_issued_count():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM issuedbooks')
    count = cursor.fetchone()[0]
    conn.close()
    return count

@app.route('/d',methods=['POST'])
def dashboard_post():
    msg=''
    if request.method == 'POST':
        session.pop('user', None)
        # Handle the form submission here
        email = request.form.get('email')
        password = request.form.get('Pas')
        print(email, password)
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()

        # Execute the query with proper placeholders
        cursor.execute('SELECT * FROM userdetails WHERE email = ? AND password = ?', (email, password))
        result = cursor.fetchone()

        if result:
            print("Login successful")
            session['userid'] = result[0]
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            print("Login failed")
            msg = 'Incorrect username/password!'

        return render_template('login.html', msg=msg)

    return render_template('login.html')
    
@app.route('/dashboard1',methods=['POST'])
def dashboard1():
    books_count = get_books_count()
    members = get_members_count()
    issued = get_issued_count()
    return render_template('dashboard.html', books_count=books_count, members=members, issued=issued)

@app.route('/das')
def das():
    books_count = get_books_count()
    members = get_members_count()
    issued = get_issued_count()
    return render_template('dashboard.html', books_count=books_count, members=members, issued=issued)






#########################################################################################################################################
#                                                   Issued
#########################################################################################################################################


def insert_issuedbook_details(mem_id, mem_name, book_id, book_title, username, date_issued, due_date):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO issuedbooks (mem_id, mem_name, book_id, title, username, date_issued, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (mem_id, mem_name, book_id, book_title, username, date_issued, due_date))
    conn.commit()
    conn.close()

def fetch_issued_books():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    # Execute a query to fetch the issued books
    cursor.execute('SELECT * FROM issuedbooks')

    # Fetch all rows from the executed query
    issued_books = cursor.fetchall()

    # Define a list to store the fetched data
    issued_books_list = []

    # Process the fetched data and add it to the list
    for book in issued_books:
        book_dict = {
            'mem_id': book[0],
            'mem_name': book[1],
            'book_id': book[2],
            'title': book[3],
            'username': book[4],
            'date_issued': book[5],
            'due_date': book[6]
        }
        issued_books_list.append(book_dict)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return issued_books_list

@app.route('/issued')
def issued():
   
    issued_books = fetch_issued_books()  # You'll need to implement this function

    return render_template('issued.html', issued_books=issued_books)


@app.route('/delete_book', methods=['POST'])
def delete_book():
    book_id = request.form.get('book_id')
    mem_id = request.form.get('mem_id')
    action= request.form.get('action')

    if action == 'return_book':
        print("Book_id=",book_id,"Member_id=",mem_id)
        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM issuedbooks WHERE mem_id = ? and book_id=?', (mem_id,book_id))
        conn.commit()
        conn.close()

    return redirect('/issued')  # Redirect to the issued page or wherever you want


    #return render_template('issued.html', issued_books=issued_books)


#########################################################################################################################################
#                                                   Issued
#########################################################################################################################################




#########################################################################################################################################
#                                                   Profile
#########################################################################################################################################

def get_user_details():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    # Assuming you're fetching details of a specific user, modify the query accordingly
    cursor.execute('SELECT username, email, password FROM users WHERE username=8848')
    user_details = cursor.fetchone()  # Assuming user_id is a variable holding the user's ID
    conn.close()

    # Convert the database result into a dictionary for easier handling
    user_dict = {
        'username': user_details[0],
        'email': user_details[1],
        'password': user_details[2]
    }

    return user_dict


def update_user_details(user_details):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute('UPDATE users SET username = ?, email = ?, password = ? WHERE username=8848',
                   (user_details['username'], user_details['email'], user_details['password']))

    conn.commit()
    conn.close()


@app.route('/profile', methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        # Handle form submission and update details in the database
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        
        user_details = get_user_details()

        # Update the user's details with the new values
        user_details['username'] = username
        user_details['email'] = email
        user_details['password'] = password

        # Update the details in the database (replace with appropriate function)
        update_user_details(user_details)

        # Redirect to the profile page to show updated details
        return redirect(url_for('profile'))

   
    user_details = get_user_details()

    # Pass the user details to the HTML template
    return render_template('profile.html', user_details=user_details)


#                                                   Profile
#########################################################################################################################################


#########################################################################################################################################
#                                                   Book Management
#########################################################################################################################################


def fetch_available_books():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    # Execute a query to fetch the issued books
    cursor.execute('SELECT * FROM books')

    # Fetch all rows from the executed query
    issued_books = cursor.fetchall()

    # Define a list to store the fetched data
    issued_books_list = []

    # Process the fetched data and add it to the list
    b = ['id', 'title', 'author', 'publisher']
    book_list = []

    for i in range(len(issued_books )):
        book_dict = {}  
        for j in range(len(b)):
            book_dict[b[j]] = issued_books [i][j] 
        book_list.append(book_dict)  

    # Create a final dictionary with the desired format
    result_dict = {'books': book_list}
    # Close the cursor and connection
    cursor.close()
    conn.close()

    return result_dict



def fetch_book_by_title(title):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Execute SQL query to select the book based on the ID
    cursor.execute('SELECT * FROM books WHERE title LIKE ?', ('%' + title + '%',))
    book_data = cursor.fetchall()
    print(book_data)
    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    b = ['id', 'title', 'author', 'publisher']
    book_list = []

    for i in range(len(book_data)):
        book_dict = {}  
        for j in range(len(b)):
            book_dict[b[j]] = book_data[i][j] 
        book_list.append(book_dict)  

    # Create a final dictionary with the desired format
    result_dict = {'books': book_list}

    # Print the resulting dictionary
    print("res:-=",result_dict,type(result_dict))
    return result_dict


def fetch_book_by_author(aname):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Execute SQL query to select the book based on the author
    cursor.execute('SELECT * FROM books WHERE author LIKE ?', ('%' + aname + '%',))
    book_data = cursor.fetchall()
    print("Data",book_data)
    # Close the cursor and connection
    cursor.close()
    conn.close()

    issued_books_list = []

    b = ['id', 'title', 'author', 'publisher']
    book_list = []

    for i in range(len(book_data)):
        book_dict = {}  
        for j in range(len(b)):
            book_dict[b[j]] = book_data[i][j] 
        book_list.append(book_dict)  

    # Create a final dictionary with the desired format
    result_dict = {'books': book_list}

    # Print the resulting dictionary
    print("res:-=",result_dict,type(result_dict))
    return result_dict


def fetch_book_by_id(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Execute SQL query to select the book based on the ID
    cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
    book_data = cursor.fetchall()
    
    print("id" ,book_data)

    b = ['id', 'title', 'author', 'publisher']
    book_list = []

    for i in range(len(book_data)):
        book_dict = {}  
        for j in range(len(b)):
            book_dict[b[j]] = book_data[i][j]  
        book_list.append(book_dict)  

    # Create a final dictionary with the desired format
    result_dict = {'books': book_list}

    # Print the resulting dictionary
    print("res:-=",result_dict,type(result_dict))
    return result_dict
    cursor.close()
    conn.close()

@app.route('/delete_book1', methods=['POST'])
def delete_book_():
    bkid = request.form.get('id')
    mem_id = request.form.get('mem_id')
    action= request.form.get('action')

    if action == 'return_book':
        print("Book_id=",bkid)
        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE id=?', (bkid,))
        conn.commit()
        conn.close()

    return redirect('/bookmanage')

@app.route('/bookmanage',methods=["GET", "POST"])
def bookmanage():
    issued_books = fetch_available_books()
    is1=[]
    issued_books_length = len(issued_books)
    bid = None
    # You'll need to implement this function
    if request.method == "POST":
        bid = request.form.get("bid")
        bname= request.form.get("bookname")
        aname = request.form.get("aname")
        if bid or bname or aname:
            
            print("Book ID:", bid)
            print("Book Name:", bname)
            print("Author Name:", aname)
            if(bid !=''):
                book = fetch_book_by_id(bid) 
                if book:
                # If a book was found with the provided ID, display only that book
                    
                    issued_books = [book]
                    print(issued_books)
                else:
                    issued_books = []
            
            elif(bname !=''):
                book = fetch_book_by_title(bname)
                print("elif",book)
                if book:
                    is1.append(book)
                    print(is1)
                    issued_books = [book]
                else:
                    issued_books = []
        
            elif(aname !=''):
                book = fetch_book_by_author(aname)
                print("before",book)
                if book:
                # If a book was found with the provided ID, display only that book
                    issued_books = [book]
                else:
                    issued_books = []
            else:
                issued_books = fetch_available_books() 
        
                # Process the fetched data and add it to the list
            #print("1",issued_books[0][1],type(issued_books))
            issued_books=issued_books[0]
            return render_template('bookmanage.html', issued_books=issued_books,issued_books_length=issued_books_length,bid=bid)
        else:
            issued_books = fetch_available_books()
            
            #print("1wc .2",issued_books)
            return render_template('bookmanage.html', issued_books=issued_books,issued_books_length=issued_books_length,bid=bid)
    else:
        issued_books = fetch_available_books()
            
        #print("1wc .2",issued_books)
        return render_template('bookmanage.html', issued_books=issued_books,issued_books_length=issued_books_length,bid=bid)




#                                                   Book Management
#########################################################################################################################################

#########################################################################################################################################
#                                                  Manage User
#########################################################################################################################################

@app.route('/manageuser')
def manageuser():
    return render_template('manageuser.html')
  
#################################################Existing Member#################################################
def fetch_members():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Execute SQL query to select member names
    cursor.execute('SELECT member_id FROM members ')

    # Fetch all rows
    member_data = cursor.fetchall()
    conn.close()
    return member_data

def fetch_member_details(member_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name, phone_number, email FROM members WHERE member_id = ?', (member_id,))
    member_data = cursor.fetchone()

    conn.close()

    if member_data:
        return {
            'name': member_data[0],
            'phone': member_data[1],
            'email': member_data[2]
        }
    else:
        return None


@app.route('/existing',methods=['GET', 'POST'])
def existing():
    members=fetch_members()
    member_data = None 
    if request.method == 'POST':
        # Handle the POST request
        mid = request.form.get('mem_id')
        member_data = fetch_member_details(mid)

        print("member:",mid)
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()

        cursor.execute('SELECT name, phone_number, email FROM members WHERE member_id = ?', (mid,))
        member_data = cursor.fetchone()
        print(member_data[1])
        if member_data:
            return render_template('existing.html', members=members, member_data=member_data)
        else:
            return render_template('existing.html', members=members)

    return render_template('existing.html', members=members)
#################################################Existing User#################################################

#################################################New User#################################################
def insert_members(name,email,phone):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO members (name,email,phone_number)
        VALUES (?, ?, ?)
    ''', (name,email,phone))
    conn.commit()
    conn.close()


@app.route('/newuser',methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        # Handle the POST request
        name = request.form.get('fname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        
    
        insert_members(name,email,phone)

          # Or use it in your logic
        return render_template('newuser.html')

    return render_template('newuser.html')

#################################################New User#################################################


#                                                  Manage User
#########################################################################################################################################


#########################################################################################################################################
#                                                  issue Books

  

def fetch_books(num_books):
    try:
        response = requests.get(api_url)
        print(api_url)
        if response.status_code == 200:
            data = response.json().get('message', [])
            print(data)
            return data[:num_books]  # Return the specified number of books
        else:
            return []

    except requests.exceptions.RequestException:
        return []

# Function to fetch book_id by book title
def fetch_book_id_by_title(book_title):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM books WHERE title = ?', (book_title,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

# Function to fetch mem_id by member name
def fetch_mem_id_by_name(name):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT member_id FROM members WHERE name = ?', (name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

# Function to insert issued book details
def insert_issuedbook_details(mem_id, mem_name, book_id, book_title, username, date_issued, due_date):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO issuedbooks (mem_id, mem_name, book_id, title, username, date_issued, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (mem_id, mem_name, book_id, book_title, username, date_issued, due_date))
    conn.commit()
    conn.close()

def fetch_titles_and_authors():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Execute SQL query to select titles and authors
    cursor.execute("SELECT title, author FROM books")

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Return titles and authors
    return rows

# Function to fetch member names from the database
def fetch_member_names():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Execute SQL query to select member names
    cursor.execute("SELECT name FROM members")

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Return member names
    return rows

@app.route('/register1', methods=['GET', 'POST'])
def register1():
    titles_and_authors = fetch_titles_and_authors()
    # Fetch member names from the database
    member_names = fetch_member_names()
    if request.method == 'POST':
        # Handle the POST request
        book_title = request.form.get('book_title')
        mem = request.form.get('mem')
        sdate = request.form.get('sdate')
        print(sdate)
        book_id = fetch_book_id_by_title(book_title)
        mem_id = fetch_mem_id_by_name(mem)
        # Calculate the due date (+5 days from the selected date)
        due_date = (datetime.datetime.strptime(sdate, '%Y-%m-%d') + datetime.timedelta(days=5)).strftime('%Y-%m-%d')

        # Insert the details into the issuedbooks table
        insert_issuedbook_details(mem_id, mem, book_id, book_title, '8848', sdate, due_date)

          
        return render_template('register1.html', titles_and_authors=titles_and_authors, member_names=member_names)
    
   
    
    return render_template('register1.html', titles_and_authors=titles_and_authors, member_names=member_names)
    return render_template("login.html")


#                                                  issue Books
#########################################################################################################################################


#########################################################################################################################################
#                                                   API page
#########################################################################################################################################
def fetch_book_details(book_id):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json().get('message', [])
            for book in data:
                if book.get('book_id') == book_id:
                    title = book.get('title')
                    author = book.get('authors')
                    publisher = book.get('publisher')
                    return title, author, publisher
        else:
            return None, None, None
    except requests.exceptions.RequestException:
        return None, None, None

    title, author, publisher = fetch_book_details(book_id)

    # Print or use the obtained details
    print('Title:', title)
    print('Author:', author)
    print('Publisher:', publisher)


def fetch_books(num_books,name,author1,publ):
    print(num_books,type(num_books))
    book_list = []
    n=int(num_books)
    try:
        
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json().get('message', [])
            print(data)
            data_len=len(data)
            conn = sqlite3.connect('books.db')
            #print("title=",title,"azuthor",author)
            cursor = conn.cursor()
            #book_list.append(response.json())# Return the specified number of books
            #print("data",data)
            books_ls=[]
            c=0
            for i in range(0,n):
                title=data[i]['title']
                author=data[i]['authors']
                publisher=data[i]['publisher']

                
                if name:
                    for i in range(0,data_len):
                        if(name in data[i]['title']):
                            na=data[i]['title']
                            a=data[i]['authors']
                            p=data[i]['publisher']
                            while (c!=n):
                                cursor.execute("INSERT INTO books (title, author, publisher) VALUES (?, ?, ?)", (na, a, p))
                                c=c+1
                if author1:
                    for i in range(0,data_len):
                        if(author1 in data[i]['authors']):
                            na=data[i]['title']
                            a=data[i]['authors']
                            p=data[i]['publisher']
                            while (c!=n):
                                cursor.execute("INSERT INTO books (title, author, publisher) VALUES (?, ?, ?)", (na, a, p))
                                c=c+1
                
                if publ:
                    for i in range(0,data_len):
                        if(publ in data[i]['publisher']):
                            na=data[i]['title']
                            a=data[i]['authors']
                            p=data[i]['publisher']
                            while (c!=n):
                                cursor.execute("INSERT INTO books (title, author, publisher) VALUES (?, ?, ?)", (na, a, p))
                                c=c+1
                
                '''
                print(books_ls)
                #print("ex",existing_book)
                for book in data:
                    for it in range(0,books_ls):
                        if book.get('bookID') == books_ls[it]:
                            title = book.get('title')
                            author = book.get('authors')
                            publisher = book.get('publisher')
                            return title, author, publisher
                '''
                '''
                cursor.execute("SELECT * FROM books WHERE title = ? AND publisher = ?", (title, author))
                existing_book = cursor.fetchone()

                # If the book doesn't already exist, insert it
                if not existing_book:
                    cursor.execute("INSERT INTO books (title, author, publisher) VALUES (?, ?, ?)", (title, author, publisher))
                '''
            conn.commit()
            conn.close()   
            #print("Tirt",book_list,"authore",book_list)
            #return book_list  # Return the specified number of books
        else:
            return []

    except requests.exceptions.RequestException:
        return []


@app.route('/api',methods=['GET', 'POST'])
def api():
    print(":")
    num_books=0
    
    if request.method == 'POST':
        print("fgjh")
        num = request.form.get('numBooks')
        name = request.form.get('name')
        author = request.form.get('author')
        publ = request.form.get('publ')
        fetch_books(num,name,author,publ)

        return render_template('api.html')
    return render_template('api.html')

#########################################################################################################################################
#                                                      About and help
#########################################################################################################################################

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/help')
def help():
    return render_template('help.html')

#########################################################################################################################################
#                                                   User Logout
#########################################################################################################################################

@app.route('/logout')
def logout():
    # Perform any logout actions if needed
    return render_template('login.html')


if __name__ == "__main__":
    app.run(port=4000)
    #app.run("0.0.0.0")
    #app.run(debug=True)
