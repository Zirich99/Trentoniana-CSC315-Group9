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
ADD CONSTRAINT audio_id FOREIGN KEY (audio_id) REFERENCES AUDIO(audio_id) ON DELETE CASCADE ON UPDATE CASCADE, 
/* MAKE THIS CHANGE FOR ALL FOREIGN KEYS ^^^ */

ADD CONSTRAINT transcript_id FOREIGN KEY (transcript_id) REFERENCES TRANSCRIPT(transcript_id) ON DELETE CASCADE ON UPDATE CASCADE, 
ADD CONSTRAINT c_name FOREIGN KEY (c_name) REFERENCES CATEGORY(c_name) ON DELETE CASCADE ON UPDATE CASCADE, 
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username) ON DELETE CASCADE ON UPDATE CASCADE
;


ALTER TABLE AUDIO 
ADD CONSTRAINT audiofile_id FOREIGN KEY (audiofile_id) REFERENCES AUDIOFILE(audiofile_id) ON DELETE CASCADE ON UPDATE CASCADE, 
ADD CONSTRAINT p_id FOREIGN KEY (p_id) REFERENCES PARTICIPANT(p_id) ON DELETE CASCADE ON UPDATE CASCADE, 
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username) ON DELETE CASCADE ON UPDATE CASCADE
; 


ALTER TABLE TRANSCRIPT 
ADD CONSTRAINT transcriptfile_id FOREIGN KEY (transcriptfile_id) REFERENCES TRANSCRIPTFILE(transcriptfile_id) ON DELETE CASCADE ON UPDATE CASCADE, 
ADD CONSTRAINT t_id FOREIGN KEY (t_id) REFERENCES TRANSCRIBER(t_id) ON DELETE CASCADE ON UPDATE CASCADE, 
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username) ON DELETE CASCADE ON UPDATE CASCADE
; 


ALTER TABLE AUDIOFILE 
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username) ON DELETE CASCADE ON UPDATE CASCADE
;


ALTER TABLE TRANSCRIPTFILE 
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username) ON DELETE CASCADE ON UPDATE CASCADE
;

ALTER TABLE PARTICIPANT
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username) ON DELETE CASCADE ON UPDATE CASCADE
;

ALTER TABLE TRANSCRIBER
ADD CONSTRAINT e_username FOREIGN KEY (e_username) REFERENCES EDITOR(e_username) ON DELETE CASCADE ON UPDATE CASCADE
;

ALTER TABLE EDITOR
ADD CONSTRAINT a_username FOREIGN KEY (a_username) REFERENCES ADMIN(a_username) ON DELETE CASCADE ON UPDATE CASCADE
;

/*
now that the Trentoniana database is fully formed,
insert example data
*/

-- create admin accts
\copy admin (a_username, a_password) FROM 'home/lion/Downloads/app/stage-v-group-9/app/ADMIN.csv' DELIMITER ',' CSV HEADER;

-- create editor accts
\copy editor (e_username, e_password, a_username) FROM 'home/lion/Downloads/app/stage-v-group-9/app/EDITOR.csv' DELIMITER ',' CSV HEADER;

-- create categories
\copy category(c_name) FROM 'home/lion/Downloads/app/stage-v-group-9/app/CATEGORY.csv' DELIMITER ',' CSV HEADER;

-- create audiofile records
\copy audiofile (audiofile_id, audio_filename, upload_date, e_username) FROM 'home/lion/Downloads/app/stage-v-group-9/app/AUDIOFILE.csv' DELIMITER ',' CSV HEADER;

-- create participants 
\copy participant(p_id, fullname, e_username) FROM 'home/lion/Downloads/app/stage-v-group-9/app/PARTICIPANT.csv' DELIMITER ',' CSV HEADER;

-- create audio records
\copy audio (audio_id, audiofile_id, date_of_recording, p_id, e_username) FROM 'home/lion/Downloads/app/stage-v-group-9/app/AUDIO.csv' DELIMITER ',' CSV HEADER;

-- create transcribers
\copy transcriber (t_id, fullname, e_username) FROM 'home/lion/Downloads/app/stage-v-group-9/app/TRANSCRIBER.csv' DELIMITER ',' CSV HEADER;

-- create transcriptfile records
\copy transcriptfile (transcriptfile_id, transcript_filename, upload_date, e_username) FROM 'home/lion/Downloads/app/stage-v-group-9/app/TRANSCRIPTFILE.csv' DELIMITER ',' CSV HEADER;

-- create transcript records
\copy transcript (transcript_id, transcriptfile_id, date_of_transcription, t_id, e_username) FROM 'home/lion/Downloads/app/stage-v-group-9/app/TRANSCRIPT.csv' DELIMITER ',' CSV HEADER;

-- create entries
\copy entry (entry_id, entry_name, audio_id, transcript_id, c_name, e_username) FROM 'home/lion/Downloads/app/stage-v-group-9/app/ENTRY.csv' DELIMITER ',' CSV HEADER;

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
