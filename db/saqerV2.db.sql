BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "settings" (
	"face_confidence"	INTEGER DEFAULT 50,
	"p_threshold"	INTEGER DEFAULT 50,
	"images_per_student"	INTEGER DEFAULT 30
);
CREATE TABLE IF NOT EXISTS "user" (
	"username"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL UNIQUE,
	"type"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("username")
);
CREATE TABLE IF NOT EXISTS "student" (
	"uni_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("uni_id")
);
CREATE TABLE IF NOT EXISTS "course" (
	"id"	INTEGER NOT NULL,
	"code"	TEXT NOT NULL UNIQUE,
	"title"	TEXT NOT NULL,
	CONSTRAINT "UNQ_course_code_title" UNIQUE("code","title"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "class" (
	"id"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"course_id"	INTEGER NOT NULL,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"instructor_id"	TEXT NOT NULL,
	CONSTRAINT "UNQ_class" UNIQUE("title","course_id","date","time"),
	CONSTRAINT "UNQ_instructor_class" UNIQUE("date","time","instructor_id"),
	FOREIGN KEY("course_id") REFERENCES "course"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("instructor_id") REFERENCES "user"("username") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "attendence" (
	"id"	INTEGER NOT NULL,
	"student_id"	INTEGER NOT NULL,
	"class_id"	INTEGER NOT NULL,
	"status"	INTEGER NOT NULL DEFAULT 1,
	CONSTRAINT "UNQ_student_attended_class" UNIQUE("student_id","class_id"),
	FOREIGN KEY("student_id") REFERENCES "student"("uni_id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("class_id") REFERENCES "class"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "behavior" (
	"id"	INTEGER NOT NULL,
	"class_id"	INTEGER NOT NULL UNIQUE,
	"happy"	REAL,
	"sad"	REAL,
	"neutral"	REAL,
	FOREIGN KEY("class_id") REFERENCES "class"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "settings" VALUES (50,50,30);
INSERT INTO "user" VALUES ('abahasn','Abdulaziz Bahasan','abahasn@iau.edu.sa','0123456',1),
 ('amhussein','Aamir Mokhtar','amhussein@iau.edu.sa','0987654',0),
 ('kawlaqi','khalid Awlaqi','kawlaqi@iau.edu.sa','0456632',1);
INSERT INTO "student" VALUES (2170003286,'Waleed'),
 (2170007761,'Omar'),
 (2170007762,'Ali');
INSERT INTO "course" VALUES (1,'CS414','Computer Organization'),
 (2,'CS411','Software Engineering'),
 (3,'CS511','Project Proposal'),
 (4,'CIS423','Web-Based Systems');
INSERT INTO "class" VALUES (1,'S7M1',2,'2020-10-11','08:00-10:00','abahasn'),
 (2,'S9M5',3,'2020-09-20','19:00-20:00','amhussein'),
 (3,'S8M2',4,'2020-03-15','10:00-12:00','abahasn'),
 (4,'S7M1',1,'2019-09-05','13:00-14:00','kawlaqi'),
 (5,'S7M1',3,'2020-10-10','09:00-10:00','amhussein'),
 (6,'S7M1',3,'2020-10-10','10:00-12:00','amhussein');
INSERT INTO "attendence" VALUES (1,2170003286,1,1),
 (2,2170007761,1,0);
INSERT INTO "behavior" VALUES (1,1,50.0,60.0,70.0);
COMMIT;
