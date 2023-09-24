import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

'''
member_id
member_name
book_title
usert_username
date_issued
'''

# Execute SQL commands to create the members table and insert data
create_table_query = """
CREATE TABLE issuedbooks (
    mem_id INTEGER ,
    mem_name TEXT,
    book_id INTEGER,
    title TEXT,
    username TEXT DEFAULT '8848',   
    date_issued DATE,
    due_date DATE
);
"""
insert_data_query="""
INSERT INTO issuedbooks(mem_id, mem_name, book_id, title, username, date_issued, due_date)
VALUES 
  (1, 'John Doe', 1, 'Harry Potter ve Sırlar Odası (Harry Potter  #2)', '8848', '2023-09-20', '2023-10-20'),
  (2, 'Alice Smith', 5, 'Echo Park (Harry Bosch  #12; Harry Bosch Universe  #16)', '8848', '2023-09-21', '2023-10-21');

"""

# Execute the SQL queries
#cursor.execute(create_table_query)
#cursor.execute(insert_data_query)
cursor.execute("select * from issuedbooks")

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
