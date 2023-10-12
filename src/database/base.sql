CREATE TABLE "song" (
	"id"	INTEGER,
	"esound_song_id"	INTEGER UNIQUE,
	"song_title"	INTEGER,
	"created_at"	DATETIME NOT NULL
	PRIMARY KEY("id" AUTOINCREMENT)
);
