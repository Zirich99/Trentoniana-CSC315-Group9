#! /usr/bin/python3

"""
ONE-TIME SETUP

To run this example in the CSC 315 VM you first need to make
the following one-time configuration changes:

# set the postgreSQL password for user 'lion'
sudo -u postgres psql
    ALTER USER lion PASSWORD 'lion';
    \q

# install pip for Python 3
sudo apt update
sudo apt install python3-pip

# install psycopg2
pip3 install psycopg2-binary

# install flask
pip3 install flask

# logout, then login again to inherit new shell environment
"""

"""
CSC 315
Spring 2021
John DeGood

# usage
export FLASK_APP=app.py 
flask run

# then browse to http://127.0.0.1:5000/

Purpose:
Demonstrate Flask/Python to PostgreSQL using the psycopg adapter.
Connects to the 7dbs database from "Seven Databases in Seven Days"
in the CSC 315 VM.

For psycopg documentation:
https://www.psycopg.org/

This example code is derived from:
https://www.postgresqltutorial.com/postgresql-python/
https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
https://www.geeksforgeeks.org/python-using-for-loop-in-flask/
"""

import psycopg2
from config import config
from flask import Flask, render_template, request

def search(userstr):
    # input: substr the user enters into the search bar
    # output: ENTRYs containing the user's search string in any of its fields
    
    # This function searches for user's input string in the fields:
    # ENTRY.entry_name
    # AUDIOFILE.audiofile_name
    # TRANSCRIPTFILE.transcriptfile_name
    # CATEGORY.c_name
    # PARTICIPANT.fullname
    # TRANSCRIBER.fullname
    # where all these values are joined by the ENTRY they relate to

    query = (
        """
SELECT
    EDITOR.e_username AS username,
    EDITOR.e_password AS password
    
FROM EDITOR
    
        """
    ).strip() # removes leading and trailing whitespace from this string

    rows = connect(query)

    # get rows containing the user string
    rows = [row for row in rows if userstr in ''.join(row) and userstr!='']

    if userstr=='':
        # user searched for empty string
        msg = [(f"Please enter a username and a password.")]
        rows.insert(0, msg)
    elif rows:
        # matches were found

        # highlight matches by surrounding them with < >
        rows = [(attr.replace(userstr, f'<{userstr}>') for attr in row) for row in rows]

        header = ('Username', 'Password')
        #cols = zip(*rows)
        #header = (attr+('_'*len(max(col,key=len))) for (attr,col) in zip(header,cols))
        rows.insert(0, header)
    elif rows==[]:  
        # no matches were found
        msg = [(f"Your username or password was incorrect.")]
        rows.insert(0, msg)
    else:
        exit("ERROR: Your database has an error. Please double check it.")

    return rows
 
 #This function combines the connections searching for a file name in the entry table
 #You will need to add a function for each query you want to make.
def connect(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters from database.ini
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()

        #The query that is automatically used to search through files
        #Rewrite this query if you want a different result
        #file_selection = "select * from entry where entry_name = '%s';" % query

        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 
# app.py

app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    return render_template('my-form.html')

# handle form data
@app.route('/form-handler', methods=['POST'])
def handle_data():
    # user input fields
    user_search = request.form['username']

    # tables whose fields you can search for a user's substring
    
    '''tables = (', ').join(request.form.getlist("search_substr"))
    if tables != '':
        # final query
        query = f"SELECT * FROM {tables};"
        # perform query
        rows = connect(query)
    else:
        rows = []'''
        
    print(search(user_search))

    rows = search(user_search)
    
    #for row in rows:
        #if rows[0] != nil && rows[1] != nil:
            #print("Login successful")

    return render_template('my-result.html', rows=rows)
    
#Router for the dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("editor_dashboard.html")


if __name__ == '__main__':
    app.run(debug = True)
