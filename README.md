# Trentoniana - CSC 315 Group 9
Group Members: Michael Mongelli, Zach Rich, Ashley Bennett, Alexandra Rizzo

## Project Description
Trentoniana is a project designed to provide the Trenton Public Library with a database for storing its audio and video files, however it is
designed to be implemented within any public or private library.
The application is a web server implemented via Python, PostgreSQL and Flask to allow users to view and modify the audio and video entries of the database.

The application allows visitors to search for entries in the database on a variety of parameters, including but not limited to entry name, topics discussed, participant name, and more. The user can also access various links connected to the Trentoniana website and other useful sources that will allow for the user to get full background on the material stored in this database.

Also included in our application are two user types: an editor and administrator. Both of these users can insert, modify, and delete entries from the database, in addition to the functions permitted for all users. The administrators are also allowed to assign new editors to the webpage, with the privilege to delete editors for any circumstance.

## Current Bugs/Limitations
The user must manually copy and paste each of the links provided in a search result to access the appropriate file.

Currently the table returned by a user's search is using a Jinja format that is barebones and lacks styling. This makes it confusing for the user to understand the results of the search.

If the user logs in with the incorrect information, they are brought to a new page instead of refreshing the current login page. An invalid/username password message should appear here.

## Installation Instructions

#### Required Programs/Applications:
Python 3 or higher - download at https://www.python.org/downloads/
PostgreSQL 12.6 or higher - download at https://www.postgresql.org/download/


#### Application Setup:
First, begin by ensuring the .csv files that contain the project data are up-to-date. These are the files that will be loaded into your application upon running the trentonian_vi.sql script.
With the data corrected you will run the trentoniana_VI.sql script in your command line. Be sure to cd to the correct location of the script.

For example, you would type the following commands into the command line if the file was located in your Downloads folder:
> cd Downloads

> psql postgres

> \i trentoniana_VI.sql

If the script was successful you should receive 10 COPY messages with a number. That number is the amount of entries that were added to the database.


Next, you will need to execute the following commands in the command line. This will allow you to make changes to the database.

> sudo -u postgres psql

> ALTER USER <username> PASSWORD <password> (where username is your system username and password is your system password>

> \q


Now you will install the Python add-ons for the project.

- Install pip for Python 3
> sudo apt update

> sudo apt install python3-pip


- Install psycopg2
> pip3 install psycopg2-binary


- Install Flask
> pip3 install flask


Logout and login to your system again, as this will allow for the Python files to be imported successfully.


### How to run the application
> start flask

> export FLASK_APP=app.py

> flask run

Browse to http://127.0.0.1:5000/. The application should be shown there if all the steps were executed correctly.
