/* Michael Mongelli, Ashley Bennett, Zachary Rich
* CSC315
* Stage V(b) 
* 
* SQL commands to create Trentoniana database,
* populate it with data from CSV files from Trentoniana,
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
    entry_name VARCHAR(255) NOT NULL PRIMARY KEY, 
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
populate the database
*/ 

\copy ADMIN(a_username, a_password) FROM '/home/lion/Desktop/stage-v-group-9/app/data/ADMIN.csv' DELIMITER ',' CSV HEADER
\copy EDITOR(e_username, e_password, a_username) FROM '/home/lion/Desktop/stage-v-group-9/app/data/EDITOR.csv' DELIMITER ',' CSV HEADER
\copy CATEGORY(c_name) FROM '/home/lion/Desktop/stage-v-group-9/app/data/CATEGORY.csv' DELIMITER ',' CSV HEADER
\copy AUDIOFILE(audiofile_id, audio_filename, upload_date, e_username) FROM '/home/lion/Desktop/stage-v-group-9/app/data/AUDIOFILE.csv' DELIMITER ',' CSV HEADER
\copy PARTICIPANT(p_id, fullname, e_username) FROM '/home/lion/Desktop/stage-v-group-9/app/data/PARTICIPANT.csv' DELIMITER ',' CSV HEADER
\copy AUDIO(audio_id, audiofile_id, date_of_recording, p_id, e_username) FROM '/home/lion/Desktop/stage-v-group-9/app/data/AUDIO.csv' DELIMITER ',' CSV HEADER
\copy TRANSCRIBER(t_id, fullname, e_username) FROM '/home/lion/Desktop/stage-v-group-9/app/data/TRANSCRIBER.csv' DELIMITER ',' CSV HEADER
\copy TRANSCRIPTFILE(transcriptfile_id, transcript_filename, upload_date, e_username) FROM '/home/lion/Desktop/stage-v-group-9/app/data/TRANSCRIPTFILE.csv' DELIMITER ',' CSV HEADER
\copy TRANSCRIPT(transcript_id, transcriptfile_id, date_of_transcription, t_id, e_username) FROM '/home/lion/Desktop/stage-v-group-9/app/data/TRANSCRIPT.csv' DELIMITER ',' CSV HEADER
\copy ENTRY(entry_id, entry_name, audio_id, transcript_id, c_name, e_username) FROM '/home/lion/Desktop/stage-v-group-9/app/data/ENTRY.csv' DELIMITER ',' CSV HEADER

\c lion