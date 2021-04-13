SELECT *
FROM AUDIOFILE
WHERE audio_filename LIKE 'Gr%';

SELECT * 
FROM ENTRY
WHERE c_name IN (SELECT *
FROM CATEGORY
WHERE c_name LIKE 'Jew%');


SELECT audiofile_id, audio_filename, upload_date
FROM AUDIOFILE
WHERE audio_filename LIKE '%Old%';


SELECT audiofile_id, audio_filename, upload_date
FROM AUDIOFILE
WHERE audio_filename LIKE '%Trenton%';


SELECT fullname, e_username 
FROM PARTICIPANT
WHERE e_username LIKE 'Editor1';


SELECT audio_id, date_of_recording, e_username
FROM AUDIO
WHERE p_id > 0;


SELECT transcript_filename, upload_date, e_username
FROM TRANSCRIPTFILE
WHERE e_username = 'Editor1';

SELECT e_username, date_of_transcription
FROM TRANSCRIPT
WHERE e_username = 'Editor1';

SELECT entry_name, c_name, e_username
FROM ENTRY
WHERE entry_id > 0;

SELECT entry_name, c_name, e_username
FROM ENTRY
WHERE entry_name LIKE '%Old%';
