#! /usr/bin/python3

# This is mikes branch

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

        print((20 * "-") + ("USER-ENTERED QUERY") + (20 * "-"))
        print(query)
        print((20 * "-") + (len("USER-ENTERED QUERY")*"-") + (20 * "-"))

        cur.execute(query)

        if 'DELETE' in query.upper():
            
            num_rows_deleted = cur.rowcount
            if num_rows_deleted > 0:
                rows = [(f"The following query was run:\n{query} deleted {num_rows_deleted} rows",)]
            else:
                rows = [("There was nothing to delete",)]

            conn.commit()
        elif 'INSERT' in query.upper():
            # 
            pass
        elif 'UPDATE' in query.upper():
            # 
            pass
        else:
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

# serve homepage when user enters site
@app.route("/")
def home_page():
    return render_template('home.html')

@app.route('/about', methods=['POST', 'GET'])
def about_page():
    if request.method == 'POST':
        return 'whats this page?'
    elif request.method == 'GET':
        return render_template('about.html')

@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        return 'so this is the login page'
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/editor-view', methods=['POST', 'GET'])
def editor_page():
    if request.method == 'POST':
        return render_template('editor.html')
    elif request.method == 'GET':
        return 'i shouldnt be here'

@app.route('/delete-result', methods=['POST'])
def delete_results_page(): # handle editor.html
    if 'submit_delete' in request.form:
        print('I GOT HERE')
        userdel = request.form['delete'] # get name of entry user wants to delete
        
        query = f"DELETE FROM CATEGORY WHERE c_name='test';"
        rows = connect(query)

        return render_template('user-result.html', rows=rows)

# handle form data
@app.route('/search', methods=['POST', 'GET']) # the page the this function leads to 
def search_page():

    if request.method == 'POST':
        return 'hello world'
    elif request.method == 'GET':
        return render_template('search.html')

@app.route('/search-result', methods=['POST'])
def search_results_page(): # handle index.html
    if 'submit_search' in request.form: #or 'submit_sort' in request.form:
        
        usersel = request.form['sort'] # get user sort selection
        userrev = True if 'reverse' in request.form else False
        sorted_rows, header = usersort(usersel, userrev) # sort db
        userstr = request.form['search'] # get user search string
        rows = usersearch(header, sorted_rows, userstr)

        return render_template('user-result.html', rows=rows)


if __name__ == '__main__':
    app.run(debug = True)

    # in case of:
    # OSError: [Errno 98] Address already in use
    # do the following:
    # $ ps -fA | grep python3
    # $ kill -9 pid
    #   where pid is the pid of the orhpaned Flask process
    # $ export FLASK_APP=app.py && flask run
    # localhost:5000 should be working again



'''
might make use of this later

tables = (', ').join(request.form.getlist("search_substr"))
    if tables != '':

        # final query
        query = f"SELECT * FROM {tables};"

        # perform query
        rows = connect(query)
    else:
        rows = []'''