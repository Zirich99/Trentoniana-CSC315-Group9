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
    search = request.form['user_search']

    # tables
    trentoniana_tables = ['Entry', 'Category']
    
    tables = []
    for table in trentoniana_tables:
        if request.form[table]=='on': tables.append(table)


    # final query
    query = f"select * from {','.join(tables)};"

    # perform query
    rows = connect(query)
    

    return render_template('my-result.html', rows=rows)
    
    def index():
        # create cursor
        cursor = conn.cursor()
        # execute select statement to fetch data to be displayed in drop-down
        cursor.execute('SELECT * FROM ENTRY')
        # fetch all rows, store as set of tuples
        rows = cursor.fetchall()
       # render template
    
    

if __name__ == '__main__':
    app.run(debug = True)
