SELECT * FROM entries WHERE date = ?

INSERT INTO entries (date, level, rain_rate, rain_acc, temperature) VALUES ()

CREATE TABLE entries (
	id INTEGER PRIMARY KEY,
	date TEXT NOT NULL,
	time TEXT NOT NULL,
	level TEXT NOT NULL,
	rain_rate TEXT,
	rain_acc TEXT,
	temperature TEXT
);