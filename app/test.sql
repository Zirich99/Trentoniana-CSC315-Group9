-- lion=> \i full/path/to/this/file.sql

DROP DATABASE IF EXISTS test;

CREATE DATABASE test;

-- connect user to new database
\c test

CREATE TABLE TEST_TABLE (
    a INT NOT NULL PRIMARY KEY,
    b INT NOT NULL,
    c INT NOT NULL
);

-- you can say TEST_TABLE or TEST_TABLE(a, b, c) to specify columns
\copy TEST_TABLE(a, b, c) FROM '/home/lion/Desktop/stage-v-group-9/app/sample.csv' DELIMITER ',' CSV HEADER