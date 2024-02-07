-- Table template

CREATE TABLE entries (
	id INTEGER PRIMARY KEY,
	date_unix INTEGER NOT NULL,
	date_text TEXT NOT NULL,
	level TEXT NOT NULL,
	rain_rate TEXT,
	rain_acc TEXT,
	temperature TEXT
);

