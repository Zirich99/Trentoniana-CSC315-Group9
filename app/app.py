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
    
# Functions to handle user input
def usersearch(header, rows, userstr):
    # input: rows returned from a previous query and the substring to search for
    # output: rows containing the user's search string in any of their fields
    
    # This function searches for user's input string in the fields:
    # ENTRY.entry_name
    # AUDIOFILE.audiofile_name
    # TRANSCRIPTFILE.transcriptfile_name
    # CATEGORY.c_name
    # PARTICIPANT.fullname
    # TRANSCRIBER.fullname
    # where all these values are joined by the ENTRY they relate to

    if userstr=='': 
        rows.insert(0, header)
        pass # if user searched for nothing, just return all rows
        # user searched for empty string
        #msg = "You did not search for anything" # message output to user
        #row = (msg,) # each row is a tuple of attrs, here just the message
        #rows = [row,] # list of rows, contains only the row with the single message item
    else:
        # get rows containing the user string
        rows = [row for row in rows if userstr in ''.join(row)]
    
        if rows:
            # matches were found

            # highlight matches by surrounding them with < >
            rows = [(attr.replace(userstr, f'<{userstr}>') for attr in row) for row in rows]

            #header = ('Title', 'Category', 'Audio File', 'Participant', 'Transcript File', 'Transcriber')
            #cols = zip(*rows)
            #header = (attr+('_'*len(max(col,key=len))) for (attr,col) in zip(header,cols))
            rows.insert(0, header)
        else:
            # no matches were found
            msg = f"No results were found containing your search '{userstr}'" # message output to user
            row = (msg,) # each row is a tuple of attrs, here just the message
            rows = [row,] # list of rows, contains only the row with the single message item

    return rows
    
def usersort(usersel, reverse):
    # input: user selection of what to sort by, chosen from dropdown
    # output: rows sorted by the chosen criteria

    # list of pairs of options with their respective column names
    options =  [('ENTRY.entry_name', 'Title'),
                ('CATEGORY.c_name', 'Category'),
                ('AUDIOFILE.audio_filename', 'Audio File'),
                ('PARTICIPANT.fullname', 'Participant'),
                ('TRANSCRIPTFILE.transcript_filename', 'Transcript File'),
                ('TRANSCRIBER.fullname', 'Transcriber')]

    # modify header to show which col the user selected to sort by
    rev = ' (reversed)' if reverse else ''
    header = tuple(f"Sorted by {col}{rev}" if opt==usersel else col for (opt,col) in options)

    # make sure all options are accounted for (except sorting by nothing)
    if usersel != '(SELECT NULL)':
        # make sure all user selection options are listed in options list,
        # catches bugs if new options are added
        if not any("Sorted by" in col for col in header):
            raise NotImplementedError(f"looks like you forgot to add option '{usersel}' to in the usersort() function")

    query = (
        f"""
SELECT
    ENTRY.entry_name AS entry,
    CATEGORY.c_name AS category,
    AUDIOFILE.audio_filename AS audio,
    PARTICIPANT.fullname AS participant,
    TRANSCRIPTFILE.transcript_filename AS transcript,
    TRANSCRIBER.fullname AS transcriber
FROM ENTRY
-- get category of entry
JOIN CATEGORY
    ON ENTRY.c_name = CATEGORY.c_name
-- get audio filename and participants
JOIN AUDIO
    ON ENTRY.audio_id = AUDIO.audio_id
JOIN AUDIOFILE
    ON AUDIO.audiofile_id = AUDIOFILE.audiofile_id
JOIN PARTICIPANT
    ON AUDIO.p_id = PARTICIPANT.p_id
-- get transcript filename and transcriber
JOIN TRANSCRIPT
    ON ENTRY.transcript_id = TRANSCRIPT.transcript_id
JOIN TRANSCRIPTFILE
    ON TRANSCRIPT.transcriptfile_id = TRANSCRIPTFILE.transcriptfile_id       
JOIN TRANSCRIBER
    ON TRANSCRIPT.t_id = TRANSCRIBER.t_id
ORDER BY {usersel} {'DESC' if reverse else 'ASC'}
;
        """
    ).strip() # removes leading and trailing whitespace from this string

    rows = connect(query)

    # add column names
    #rows.insert(0, header)

    return rows, header
 
 #This function combines the connections searching for a file name in the entry table
 #You will need to add a function for each query you want to make.
def connect(query):
    # ADDED: initialize output to None
    #output = None
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
        print('Test1', '*' *50)
        cur.execute(query)
        print('Test2', '*' *50)
        #output= cur.fetchone()
        #while output is not None:
        #    print(output)
        #    output = DBCursor.fetchone()
        rows = cur.fetchall()
        print('Test3', '*' *50)

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()

    #return output
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
    # error field
    error = None
    # user input fields
    user_login = request.form['username']
    user_password = request.form['password']
    
    #Final query
    query = f"SELECT e_username, e_password FROM EDITOR WHERE e_username LIKE '{user_login}' AND e_password LIKE '{user_password}'"
    
    #Perform the query
    result = connect(query)
    
    if result == []:
        error = 'Invalid username or password'
        print("ERROR!")
        return render_template('my-form.html', error=error)
    else:
        print("CORRECT!")
        return render_template('editor-dashboard.html', result=result)
    
#Router for the dashboard
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'submit_search' in request.form: #or 'submit_sort' in request.form:
        print("Search request received")
        usersel = request.form['sort'] # get user sort selection
        print("User sort")
        userrev = True if 'reverse' in request.form else False
        sorted_rows, header = usersort(usersel, userrev) # sort db
        userstr = request.form['search'] # get user search string
        print("Found user string")
        rows = usersearch(header, sorted_rows, userstr) 
        return render_template('my-result.html', rows=rows)
        
    return render_template('editor-dashboard.html')

# Route to get to insertion page
@app.route('/insert-entry', methods=['POST'])
def insert_page():
    # user input fields
    insert_ = request.form['insert']
    #insert_value = 
    #Final query
    query = f"INSERT INTO '{user_insert}' VALUES '{user_insert}"
    #Perform the query
    result = connect(query)
    
    if result == []:
        error = 'Invalid insertion'
        print("ERROR!")
        return render_template('editor-dashboard.html', error=error)
    else:
        print("CORRECT!")
        return render_template('editor-insert.html', result=result)


#delete function instead of connect
def deleton(query):
    conn = None
    rows_deleted = 0
    try:
        #read connection parameters from database.ini
        params = config()
        
        #connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('4 new test hi')
        print('Connected.')

        #create a cursor
        cur = conn.cursor()
        print('5 test hey')

        #execute the DELETE statement
        cur.execute("DELETE FROM entry WHERE entry_name LIKE %s", (query))

        #get the number of updated rows
        rows_deleted = cur.rowcount
        print('6 TEST')

        #commit the changes to the database
        conn.commit()

        #Close communication with PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows_deleted


@app.route('/delete-entry', methods=['POST'])
def delete():
    #User input to delete
    delete_entry = request.form['delete']
    #Query
    #query = f"DELETE FROM ENTRY WHERE entry_name LIKE '{delete_entry}'"
    query = [delete_entry]
    #Perform query
    deleton(query)
    if delete_entry =="":
        error = 'Invalid entry, please try again.'
        return render_template('editor-dashboard.html', error=error)
    else:
        return render_template('editor-deletion.html', delete_entry=delete_entry)


#ex DELETE FROM "" WHERE gbfs='vda';

if __name__ == '__main__':
    app.run(debug = True)
