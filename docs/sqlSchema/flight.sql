DROP TABLE if exists flights;
CREATE TABLE flights(
    id          INTEGER PRIMARY KEY NOT NULL,
    number      INTEGER NOT NULL,
    hash        VARCHAR(50) NOT NULL,
    start_date  DATETIME
);
CREATE INDEX fligh_number ON flights;
