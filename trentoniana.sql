/* Michael Mongelli, Ashley Bennett, Zachary Rich
* CSC315
* Stage V(a) 
* 
* SQL commands to create Trentoniana database,
* populate it with example data,
* and perform queries on the data */

DROP DATABASE IF EXISTS trentoniana;

CREATE DATABASE trentoniana;

-- connect user to new database
\c trentoniana

/*
Initialize all tables (without foreign keys):
ENTRY, CATEGORY,
AUDIO, TRANSCRIPT, 
AUDIOFILE, TRANSCRIPTFILE,
PARTICIPANT, TRANSCRIBER,
ADMIN, EDITOR
*/

CREATE TABLE ENTRY (
    entry_id INT NOT NULL PRIMARY KEY,
    entry_name VARCHAR(255) NOT NULL, 
    audio_id INT NOT NULL, -- AUDIO
    transcript_id INT NOT NULL, -- TRANSCRIPT
    c_name VARCHAR(255) NOT NULL, -- CATEGORY
    e_username VARCHAR(255) NOT NULL -- EDITOR
);

CREATE TABLE CATEGORY (
    c_name VARCHAR(255) NOT NULL PRIMARY KEY
);

CREATE TABLE AUDIO (
    audio_id INT NOT NULL PRIMARY KEY,
    audiofile_id INT NOT NULL, -- AUDIOFILE
    date_of_recording DATE NOT NULL,
    p_id INT NOT NULL, -- PARTICIPANT
    e_username VARCHAR(255) NOT NULL -- EDITOR
);

CREATE TABLE TRANSCRIPT (
    transcript_id INT NOT NULL PRIMARY KEY,
    transcriptfile_id INT NOT NULL, -- TRANSCRIPTFILE
    date_of_transcription DATE NOT NULL,
    t_id INT NOT NULL, -- TRANSCRIBER
    e_username VARCHAR(255) NOT NULL -- EDITOR
);

CREATE TABLE AUDIOFILE (
    audiofile_id INT NOT NULL PRIMARY KEY,
    audio_filename VARCHAR(255) NOT NULL,
    upload_date DATE NOT NULL,
    e_username VARCHAR(255) NOT NULL -- EDITOR
);

CREATE TABLE TRANSCRIPTFILE (
    transcriptfile_id INT NOT NULL PRIMARY KEY,
    transcript_filename VARCHAR(255) NOT NULL,
    upload_date DATE NOT NULL,
    e_username VARCHAR(255) NOT NULL -- EDITOR
);

CREATE TABLE PARTICIPANT (
    p_id INT NOT NULL PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    e_username VARCHAR(255) NOT NULL -- EDITOR
);

CREATE TABLE TRANSCRIBER (
    t_id INT NOT NULL PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    e_username VARCHAR(255) NOT NULL -- EDITOR
);

CREATE TABLE ADMIN (
    a_username VARCHAR(255) NOT NULL PRIMARY KEY,
    a_password VARCHAR(255) NOT NULL
);

CREATE TABLE EDITOR (
    e_username VARCHAR(255) NOT NULL PRIMARY KEY,
    e_password VARCHAR(255) NOT NULL,
    a_username VARCHAR(255) NOT NULL -- ADMIN
);



/*
Now that all tables have been initialized, 
add foreign keys between tables
*/

ALTER TABLE ENTRY 
ADD CONSTRAINT audio_id FOREIGN KEY (audio_id) REFERENCES AUDIO(audio_id), 
ADD CONSTRAINT transcript_id FOREIGN KEY (transcript_id) REFERENCES TRANSCRIPT(transcript_id), 
ADD CONSTRAINT c_name FOREIGN KEY (c_name) REFERENCES CATEGORY(c_name), 
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username)
;


ALTER TABLE AUDIO 
ADD CONSTRAINT audiofile_id FOREIGN KEY (audiofile_id) REFERENCES AUDIOFILE(audiofile_id), 
ADD CONSTRAINT p_id FOREIGN KEY (p_id) REFERENCES PARTICIPANT(p_id), 
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username)
; 


ALTER TABLE TRANSCRIPT 
ADD CONSTRAINT transcriptfile_id FOREIGN KEY (transcriptfile_id) REFERENCES TRANSCRIPTFILE(transcriptfile_id), 
ADD CONSTRAINT t_id FOREIGN KEY (t_id) REFERENCES TRANSCRIBER(t_id), 
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username)
; 


ALTER TABLE AUDIOFILE 
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username)
;


ALTER TABLE TRANSCRIPTFILE 
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username)
;

ALTER TABLE PARTICIPANT
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username)
;

ALTER TABLE TRANSCRIBER
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username)
;

ALTER TABLE EDITOR
ADD CONSTRAINT a_username FOREIGN KEY (a_username) REFERENCES ADMIN(a_username)
;

/*
now that the Trentoniana database is fully formed,
insert example data
*/

-- create admin accts
INSERT INTO admin (a_username, a_password)
VALUES ('Admin1', 'adminpassword1');
INSERT INTO admin (a_username, a_password)
VALUES ('Admin2', 'adminpassword2');
INSERT INTO admin (a_username, a_password)
VALUES ('Admin3', 'adminpassword3');

-- create editor accts
INSERT INTO editor (e_username, e_password, a_username)
VALUES ('Editor1', 'editorpassword1', 'Admin1');
INSERT INTO editor (e_username, e_password, a_username)
VALUES ('Editor2', 'editorpassword2', 'Admin1');
INSERT INTO editor (e_username, e_password, a_username)
VALUES ('Editor3', 'editorpassword3', 'Admin2');

-- create categories
INSERT INTO category(c_name)
VALUES ('Jewish');
INSERT INTO category(c_name)
VALUES ('Oral History');
INSERT INTO category(c_name)
VALUES ('Family History');
INSERT INTO category(c_name)
VALUES ('Immigration');

-- create audiofile records
INSERT INTO audiofile (audiofile_id, audio_filename, upload_date, e_username)
VALUES (8, 'JHS08', '04/11/2021', 'Editor1');
INSERT INTO audiofile (audiofile_id, audio_filename, upload_date, e_username)
VALUES (1, 'Grace Womack and Jean Lynch', '04/11/2021', 'Editor1');
INSERT INTO audiofile (audiofile_id, audio_filename, upload_date, e_username)
VALUES (2, 'Old Trenton Oral History Sudol Edwards', '04/11/2021', 'Editor1');

-- create participants 
INSERT INTO participant(p_id, fullname, e_username)
VALUES (1, 'JoeKlatzkin', 'Editor1');
INSERT INTO participant(p_id, fullname, e_username)
VALUES (2, 'IdaKlatzkin', 'Editor1');
INSERT INTO participant
(p_id, fullname, e_username)
VALUES (3, 'Grace Womack', 'Editor1');
INSERT INTO participant
(p_id, fullname, e_username)
VALUES (4, 'Jean Lynch', 'Editor1');
INSERT INTO participant
(p_id, fullname, e_username)
VALUES (5, 'Sudol Edwards', 'Editor1');

-- create audio records
INSERT INTO audio (audio_id, audiofile_id, date_of_recording, p_id, e_username)
VALUES (8, 8, '06/08/1988', 1, 'Editor1');
INSERT INTO audio (audio_id, audiofile_id, date_of_recording, p_id, e_username)
VALUES (1, 1, '04/14/2015', 3, 'Editor1');
INSERT INTO audio (audio_id, audiofile_id, date_of_recording, p_id, e_username)
VALUES (2, 2, '06/09/2016', 5, 'Editor1');

-- create transcribers
INSERT INTO transcriber (t_id, fullname, e_username)
VALUES (1, 'John Smith', 'Editor1');
INSERT INTO transcriber (t_id, fullname, e_username)
VALUES (2, 'Jane Doe', 'Editor2');
INSERT INTO transcriber (t_id, fullname, e_username)
VALUES (3, 'Alexandra Rizzo', 'Editor3');

-- create transcriptfile records
INSERT INTO transcriptfile (transcriptfile_id, transcript_filename, upload_date, e_username)
VALUES (8, 'Klatzkin, Joe & Ida', '4/11/2021', 'Editor1');
INSERT INTO transcriptfile (transcriptfile_id, transcript_filename, upload_date, e_username)
VALUES (1, 'Grace Womack and Jean Lynch 4 14 15', '4/11/2021', 'Editor1');
INSERT INTO transcriptfile (transcriptfile_id, transcript_filename, upload_date, e_username)
VALUES (2, 'Sudol Edwards', '4/11/2021', 'Editor1');

-- create transcript records
INSERT INTO transcript (transcript_id, transcriptfile_id, date_of_transcription, t_id, e_username)
VALUES (8, 8, '2021-04-11', 1, 'Editor1');
INSERT INTO transcript (transcript_id, transcriptfile_id, date_of_transcription, t_id, e_username)
VALUES (1, 1, '2021-04-11', 1, 'Editor1');
INSERT INTO transcript (transcript_id, transcriptfile_id, date_of_transcription, t_id, e_username)
VALUES (2, 2, '2021-04-11', 2, 'Editor1');

-- create entries
INSERT INTO entry (entry_id, entry_name, audio_id, transcript_id, c_name, e_username)
VALUES (8, 'JHS 08', 8, 8, 'Jewish', 'Editor1');
INSERT INTO entry (entry_id, entry_name, audio_id, transcript_id, c_name, e_username)
VALUES (1, 'Old Trenton Oral History, 4-14-15', 1, 1, 'Oral History', 'Editor1');
INSERT INTO entry (entry_id, entry_name, audio_id, transcript_id, c_name, e_username)
VALUES (2, 'Old Trenton Oral History Sudol Edwards', 2, 2, 'Oral History', 'Editor1');

/*
perform queries on populated database
*/

\echo 'Search for audiofiles starting with "Gr": '
SELECT *
FROM AUDIOFILE
WHERE audio_filename LIKE 'Gr%';

\echo 'Search entries containing Jewish oral histories: '
SELECT * 
FROM ENTRY
WHERE c_name IN (SELECT *
FROM CATEGORY
WHERE c_name LIKE 'Jew%');

\echo 'Search audiofiles containing search string "Old": '
SELECT audiofile_id, audio_filename, upload_date
FROM AUDIOFILE
WHERE audio_filename LIKE '%Old%';

\echo 'Search audiofiles containing search string "Trenton": '
SELECT audiofile_id, audio_filename, upload_date
FROM AUDIOFILE
WHERE audio_filename LIKE '%Trenton%';

\echo 'Search for participant profiles created by Editor1: '
SELECT fullname, e_username
FROM PARTICIPANT
WHERE e_username LIKE 'Editor1';

\echo 'Search for transcripts editted by Editor1: '
SELECT transcript_filename, upload_date, e_username
FROM TRANSCRIPTFILE
WHERE e_username = 'Editor1';

\echo 'Search for entries containing string "Old" in title: '
SELECT entry_name, c_name, e_username
FROM ENTRY
WHERE entry_name LIKE '%Old%';
