BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "settings" (
	"detectionConfidence"	INTEGER DEFAULT 50,
	"recognitionThreshold"	INTEGER DEFAULT 50,
	"imagesPerStudent"	INTEGER DEFAULT 30
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
	"universityId"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("universityId")
);
CREATE TABLE IF NOT EXISTS "student_photos" (
	"studentId"	INTEGER NOT NULL,
	"photoURL"	TEXT NOT NULL UNIQUE,
	FOREIGN KEY("studentId") REFERENCES "student"("universityId") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("studentId")
);
CREATE TABLE IF NOT EXISTS "course" (
	"Id"	INTEGER NOT NULL,
	"code"	TEXT NOT NULL UNIQUE,
	"title"	TEXT NOT NULL,
	CONSTRAINT "UNQ_course_code_title" UNIQUE("code","title"),
	PRIMARY KEY("Id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "class" (
	"Id"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"courseId"	INTEGER NOT NULL,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"instructorUsername"	TEXT NOT NULL,
	CONSTRAINT "UNQ_class" UNIQUE("title","courseId","date","time"),
	CONSTRAINT "UNQ_instructor_class" UNIQUE("date","time","instructorUsername"),
	FOREIGN KEY("courseId") REFERENCES "course"("Id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("instructorUsername") REFERENCES "user"("username") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "attendence" (
	"Id"	INTEGER NOT NULL,
	"studentId"	INTEGER NOT NULL,
	"classId"	INTEGER NOT NULL,
	"status"	INTEGER NOT NULL DEFAULT 1,
	CONSTRAINT "UNQ_student_attended_class" UNIQUE("studentId","classId"),
	FOREIGN KEY("studentId") REFERENCES "student"("universityId") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("classId") REFERENCES "class"("Id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "behavior" (
	"Id"	INTEGER NOT NULL,
	"classId"	INTEGER NOT NULL UNIQUE,
	"B1%"	REAL,
	"B2%"	REAL,
	"B3%"	REAL,
	"B4%"	REAL,
	"B5%"	REAL,
	FOREIGN KEY("classId") REFERENCES "class"("Id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Id" AUTOINCREMENT)
);
INSERT INTO "settings" VALUES (50,50,30);
INSERT INTO "user" VALUES ('abahasn','Abdulaziz Bahasan','abahasn@iau.edu.sa','0123456',1),
 ('amhussein','Aamir Mokhtar','amhussein@iau.edu.sa','0987654',0),
 ('kawlaqi','khalid Awlaqi','kawlaqi@iau.edu.sa','0456632',1);
INSERT INTO "student" VALUES (2170003286,'Waleed'),
 (2170007761,'Omar');
INSERT INTO "student_photos" VALUES (2170003286,'file:///C:/Users/lenovo-pc/Desktop/IAU/GP 2020-2021/CS-511/Team Work/Charts/ER Diagram (SDS)/ERD all-Page-2.png'),
 (2170007761,'file:///C:/Users/lenovo-pc/Desktop/IAU/GP 2020-2021/CS-511/Team Work/Images/face-detection.png');
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
INSERT INTO "behavior" VALUES (1,1,50.0,60.0,70.0,80.0,90.0);
COMMIT;
