CREATE TABLE `values` (
	`id`	INTEGER NOT NULL,
	`value`	INTEGER NOT NULL,
	`name`	TEXT,
	`unit`	TEXT,
	`parameter_id`	INTEGER,
	PRIMARY KEY(`id`),
    FOREIGN KEY parameter_id REFERENCES parameters(id)
);