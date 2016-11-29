DROP TABLE if EXISTS parameters;
CREATE TABLE parameters (
    id          INTEGER PRIMARY KEY NOT NULL,
    type        VARCHAR(20),
    source      VARCHAR(20),

    validated   BOOLEAN,
    valid       BOOLEAN,

    time_received   DATETIME,
    time_created    DATETIME,

    flight_id INTEGER NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES flights(id)
);