CREATE TABLE IF NOT EXISTS "aircraft" (
	"aircraft_id"	INTEGER NOT NULL UNIQUE,
	"manufacturer"	VARCHAR(50) NOT NULL,
	"aircraft_model"	VARCHAR(50) NOT NULL,
	"aircraft_registration"	VARCHAR(10) NOT NULL,
	PRIMARY KEY("aircraft_id" AUTOINCREMENT),
	FOREIGN KEY("manufacturer") REFERENCES "aircraft_type"("manufacturer"),
	FOREIGN KEY("aircraft_model") REFERENCES "aircraft_type"("aircraft_model")
);
CREATE TABLE IF NOT EXISTS "aircraft_type" (
	"manufacturer"	VARCHAR(50) NOT NULL,
	"aircraft_model"	VARCHAR(50) NOT NULL,
	"maximum_capacity"	INTEGER NOT NULL,
	"maximum_range"	INTEGER NOT NULL,
	PRIMARY KEY("manufacturer","aircraft_model")
);
CREATE TABLE IF NOT EXISTS "flight" (
	"flight_id"	INTEGER NOT NULL UNIQUE,
	"flight_designator"	VARCHAR(6) NOT NULL,
	"aircraft_id"	INTEGER NOT NULL,
	"departure"	DATETIME NOT NULL,
	"arrival"	DATETIME NOT NULL,
	"departure_airport_code"	VARCHAR(3) NOT NULL,
	"arrival_airport_code"	VARCHAR(3) NOT NULL,
	"passengers"	INTEGER NOT NULL,
	PRIMARY KEY("flight_id" AUTOINCREMENT),
	FOREIGN KEY("aircraft_id") REFERENCES "aircraft"("aircraft_id")
);
CREATE TABLE IF NOT EXISTS "flight_pilot_link_table" (
	"pilot_id"	INTEGER NOT NULL,
	"flight_id"	INTEGER NOT NULL,
	PRIMARY KEY("pilot_id","flight_id"),
	FOREIGN KEY("pilot_id") REFERENCES "pilot"("pilot_id"),
	FOREIGN KEY("flight_id") REFERENCES "flight"("flight_id")
);
CREATE TABLE IF NOT EXISTS "pilot" (
	"pilot_id"	INTEGER NOT NULL UNIQUE,
	"first_name"	VARCHAR(50) NOT NULL,
	"last_name"	VARCHAR(50) NOT NULL,
	"nationality"	VARCHAR(50),
	"license_number"	VARCHAR(50) NOT NULL,
	"license_expirydate"	DATE NOT NULL,
	"flight_hours"	INTEGER NOT NULL,
	PRIMARY KEY("pilot_id" AUTOINCREMENT)
);

