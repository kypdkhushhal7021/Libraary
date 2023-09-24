from flask import Flask, render_template, request, session, url_for, redirect, jsonify, make_response, flash
import sqlite3
import datetime
import random
import requests
app = Flask(__name__)



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
'''
def get_members_count():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM members')
    count = cursor.fetchone()[0]
    conn.close()
    return members_count
'''
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

        # Perform any necessary processing based on the form data

        # Redirect to the appropriate page after form submission
        #return redirect(url_for('dashboard1'))

    # Handle other cases if needed
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


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/help')
def help():
    return render_template('help.html')



def insert_issuedbook_details(mem_id, mem_name, book_id, book_title, username, date_issued, due_date):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO issuedbooks (mem_id, mem_name, book_id, title, username, date_issued, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (mem_id, mem_name, book_id, book_title, username, date_issued, due_date))
    conn.commit()
    conn.close()


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
        
        # Calculate the due date (+5 days from the selected date)
        # Insert the details into the issuedbooks table
        insert_members(name,email,phone)

          # Or use it in your logic
        return render_template('newuser.html')




    
    return render_template('newuser.html')













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

    # Assuming 'users' table has columns: id, fname, email, password
    # Assuming user_details is a dictionary containing user details
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

        # Fetch the current user's details from the database
        # Replace 'get_user_details()' with an appropriate function to get user details
        user_details = get_user_details()

        # Update the user's details with the new values
        user_details['username'] = username
        user_details['email'] = email
        user_details['password'] = password

        # Update the details in the database (replace with appropriate function)
        update_user_details(user_details)

        # Redirect to the profile page to show updated details
        return redirect(url_for('profile'))

    # Fetch current user details from the database (assuming you have a function to do this)
    # Replace 'get_user_details()' with an appropriate function to get user details
    user_details = get_user_details()

    # Pass the user details to the HTML template
    return render_template('profile.html', user_details=user_details)


@app.route('/manageuser')
def manageuser():
    return render_template('manageuser.html')





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
    for book in issued_books:
        book_dict = {
            'id': book[0],
            'title': book[1],
            'author': book[2],
            'publisher': book[3]
           
        }
        issued_books_list.append(book_dict)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return issued_books_list



def fetch_book_by_title(title):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Execute SQL query to select the book based on the ID
    cursor.execute('SELECT * FROM books WHERE title LIKE ?', ('%' + title + '%',))
    book_data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the book data if found, or None if not found
    if book_data:
        book_dict = {
            'id': book_data[0],
            'title': book_data[1],
            'author': book_data[2],
            'publisher': book_data[3]
        }
        return book_dict
    else:
        return None
def fetch_book_by_author(aname):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Execute SQL query to select the book based on the ID
    cursor.execute('SELECT * FROM books WHERE author LIKE ?', ('%' + aname + '%',))
    book_data = cursor.fetchall()


    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the book data if found, or None if not found
    if book_data:
        book_dict = {
            'id': book_data[0],
            'title': book_data[1],
            'author': book_data[2],
            'publisher': book_data[3]
        }
        return book_dict
    else:
        return None
def fetch_book_by_id(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Execute SQL query to select the book based on the ID
    cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
    book_data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the book data if found, or None if not found
    if book_data:
        book_dict = {
            'id': book_data[0],
            'title': book_data[1],
            'author': book_data[2],
            'publisher': book_data[3]
        }
        return book_dict
    else:
        return None


@app.route('/bookmanage',methods=["GET", "POST"])
def bookmanage():
    issued_books = fetch_available_books()
    bid = None
    # You'll need to implement this function
    if request.method == "POST":
        bid = request.form.get("bookid")
        bname= request.form.get("bookname")
        aname = request.form.get("Aname")
        if bid or bname or aname:
            # At least one of the values is not empty, handle accordingly
            # For example, print the values
            print("Book ID:", bid)
            print("Book Name:", bname)
            print("Author Name:", aname)
            if(bid !=''):
                book = fetch_book_by_id(bid) 
                if book:
                # If a book was found with the provided ID, display only that book
                    issued_books = [book]
                else:
                    issued_books = []
            
            elif(bname !=''):
                book = fetch_book_by_title(bname) 
                if book:
                # If a book was found with the provided ID, display only that book
                    issued_books = [book]
                else:
                    issued_books = []
        
            elif(aname !=''):
                book = fetch_book_by_author(aname) 
                if book:
                # If a book was found with the provided ID, display only that book
                    issued_books = [book]
                else:
                    issued_books = []
            else:
                issued_books = fetch_available_books() 
        else:
            issued_books = fetch_available_books()
                # Fetch all rows
        

                # Process the fetched data and add it to the list
                
        return render_template('bookmanage.html', issued_books=issued_books,bid=bid)
    return render_template('bookmanage.html', issued_books=issued_books,bid=bid)
       











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

          # Or use it in your logic
        return render_template('register1.html', titles_and_authors=titles_and_authors, member_names=member_names)
    
    # Handle the GET request
    # Fetch titles and authors from the database
    
    return render_template('register1.html', titles_and_authors=titles_and_authors, member_names=member_names)
    return render_template("login.html")
'''
@app.route('/iss', methods=["GET", "POST"])
def issue():
    # Fetch titles and authors from the database
    titles_and_authors = fetch_titles_and_authors()

    # Fetch member names from the database
    member_names = fetch_member_names()

    return render_template('issue.html', titles_and_authors=titles_and_authors, member_names=member_names)
    return render_template("login.html")
'''

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
@app.route('/register', methods=["GET", "POST"])
def register():
    
    return render_template('register.html')
    return render_template("login.html")

@app.route('/logout')
def logout():
    # Perform any logout actions if needed
    return render_template('login.html')


def fetch_books(num_books):
    book_list = [] 
    try:
        print("done")
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json().get('message', [])
            #book_list.append(response.json())# Return the specified number of books
            #print("data",data)
            for i in range(0,5):
                title=data[i]['title']
                author=data[i]['authors']
                publisher=data[i]['publisher']
                #book_list.append(t)
                #book_list.append(a)
            conn = sqlite3.connect('books.db')
            print("title=",title,"azuthor",author)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (title,author,publisher)
                VALUES (?, ?, ?)
            ''', (title,author,publisher))
            conn.commit()
            conn.close()   
            #print("Tirt",book_list,"authore",book_list)
            #return book_list  # Return the specified number of books
        else:
            return []

    except requests.exceptions.RequestException:
        return []


def insert_members(name,email,phone):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO members (name,email,phone_number)
        VALUES (?, ?, ?)
    ''', (name,email,phone))
    conn.commit()
    conn.close()




@app.route('/api')
def api():
    
    num_books=0
    books = fetch_books(num_books)
    if request.method == 'POST':
        # Handle the POST request
        title = request.form.get('title')
        publisher = request.form.get('publisher')
        author = request.form.get('author')
        
        # Calculate the due date (+5 days from the selected date)
        # Insert the details into the issuedbooks table
        insert_members(title,author,publisher)

          # Or use it in your logic
        return render_template('newuser.html')
    return render_template('api.html')

'''
@app.route('/api', methods=['GET'])
def import_books():
    num_books = int(request.args.get('num_books'))
    books = fetch_books(num_books)
    return jsonify(books)
'''
'''
@app.route('/login', methods=["GET", "POST"])
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
            return redirect(url_for('login'))
        else:
            print("Login failed")
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)

    return render_template('login.html')

#########################################################################################################################################
#                                               gov policies
#########################################################################################################################################


@app.route('/weth1')
def weth1():
    return render_template('wethprediction.html')
#########################################################################################################################################
#                                               gov policies
#########################################################################################################################################


@app.route('/pol')
def policy():
    return render_template('pol.html')
#########################################################################################################################################
#                                                   Index page
#########################################################################################################################################




@app.route('/about')
def about():
    return render_template('about.html')
#########################################################################################################################################
#                                                   User page
#########################################################################################################################################


@app.route('/contact')
def contact():
    
    print(request.form.get("lang"))
    print("hi")
    return render_template('contact.html')
#########################################################################################################################################
#                                                   User Logout
#########################################################################################################################################


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('login'))


#########################################################################################################################################
#                                                 Database COnnection
#########################################################################################################################################

def dbConnection():
    return sqlite3.connect('books.db')
def dbClose(con):
    if con:
        con.close()

#########################################################################################################################################
#                                                   User Registeration
#########################################################################################################################################


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print(request.form.get("lang"))
        try:
            status = ""
            name = request.form.get("Name")
            Email = request.form.get("Email")
            pass1 = request.form.get("pass1")
            con = dbConnection()
            cursor = con.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE email = ?', (Email,))
            res = cursor.fetchone()
            #res = 0
            if not res:
                cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, Email, pass1))
                con.commit()
                status = "success"
                return redirect(url_for('dashboard'))
            else:
                status = "Already available"
            # return status
            return redirect(url_for('dashboard'))
        except:
            print("Exception occured at user registration",str(e))
            return redirect(url_for('dashboard'))
        finally:
            dbClose(con)
    return render_template('register.html')
#########################################################################################################################################
#                                                   User Login
#########################################################################################################################################


@app.route('/login', methods=["GET", "POST"])
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
#                                                      Home page
#########################################################################################################################################


@app.route('/home.html')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return render_template("dashboard.html")
'''
if __name__ == "__main__":
    app.run(port=4000)
    #app.run("0.0.0.0")
    #app.run(debug=True)
