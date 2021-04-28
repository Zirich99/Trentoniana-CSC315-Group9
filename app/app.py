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
;
        """
    ).strip() # removes leading and trailing whitespace from this string

    rows = connect(query)

    # get rows containing the user string
    rows = [row for row in rows if userstr in ''.join(row)]

    if userstr=='':
        # user searched for empty string
        msg = [(f"You did not search for anything")]
        rows.insert(0, msg)
    elif rows:
        # matches were found

        # highlight matches by surrounding them with < >
        rows = [(attr.replace(userstr, f'<{userstr}>') for attr in row) for row in rows]

        header = ('Entry', 'Category', 'Audio', 'Participant', 'Transcript', 'Transcriber')
        #cols = zip(*rows)
        #header = (attr+('_'*len(max(col,key=len))) for (attr,col) in zip(header,cols))
        rows.insert(0, header)
    elif rows==[]:  
        # no matches were found
        msg = [(f"No entries were found containing your search '{userstr}'")]
        rows.insert(0, msg)
    else:
        exit("idk what this case means")

    return rows

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
    user_select = request.form['sortchoice']
    if user_select == "Category":
        query = """
        SELECT 
        entry_name, ENTRY.c_name
        FROM CATEGORY 
        JOIN ENTRY ON ENTRY.c_name= CATEGORY.c_name

        SELECT (SELECT entry_name, ENTRY.c_name
        FROM CATEGORY)
        (SELECT audio_id, ENTRY.audio_id
        FROM CATEGORY);"""
        
        
        rows = connect(query)
        header = ("""'entry_name', 'c_name', 'audio_filename',
        'participant_fullname', 'transcript_filename', 
        'transcriber_fullname'""")
    
        
    return render_template('my-result.html', rows=rows)
   
#Route to about us page

@app.route('/about-us', methods=['POST'])
def about_but():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug = True)
