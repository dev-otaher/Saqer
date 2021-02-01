BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "settings" (
	"detection_confidence"	INTEGER DEFAULT 50,
	"recogintion_threshold"	INTEGER DEFAULT 50,
	"image_per_student"	INTEGER DEFAULT 30
);
CREATE TABLE IF NOT EXISTS "student" (
	"uid"	INTEGER NOT NULL,
	"Sname"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("uid")
);
CREATE TABLE IF NOT EXISTS "attendence" (
	"aid"	INTEGER NOT NULL,
	"a_stu_id"	INTEGER NOT NULL,
	"a_class_id"	INTEGER NOT NULL,
	"status"	INTEGER NOT NULL DEFAULT 1 COLLATE BINARY,
	FOREIGN KEY("a_stu_id") REFERENCES "student"("uid") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("a_class_id") REFERENCES "class"("sid") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "UNQ_student_attended_class" UNIQUE("a_stu_id","a_class_id"),
	PRIMARY KEY("aid" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "behavior" (
	"bid"	INTEGER NOT NULL,
	"b_class_id"	INTEGER NOT NULL UNIQUE,
	"b1%"	REAL,
	"b2%"	REAL,
	"b3%"	REAL,
	"b4%"	REAL,
	"b5%"	REAL,
	FOREIGN KEY("b_class_id") REFERENCES "class"("sid") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("bid" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "user" (
	"username"	TEXT NOT NULL,
	"Uname"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL UNIQUE,
	"type"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("username")
);
CREATE TABLE IF NOT EXISTS "student_photos" (
	"student_id"	INTEGER NOT NULL,
	"img_url"	TEXT NOT NULL UNIQUE,
	FOREIGN KEY("student_id") REFERENCES "student"("uid") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("student_id")
);
CREATE TABLE IF NOT EXISTS "course" (
	"cid"	INTEGER NOT NULL,
	"code"	TEXT NOT NULL UNIQUE,
	"ctitle"	TEXT NOT NULL,
	CONSTRAINT "UNQ_course_code_title" UNIQUE("code","ctitle"),
	PRIMARY KEY("cid" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "class" (
	"sid"	INTEGER NOT NULL,
	"stitle"	TEXT NOT NULL,
	"course_id"	INTEGER NOT NULL,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"instructor"	TEXT NOT NULL,
	FOREIGN KEY("instructor") REFERENCES "user"("username") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("course_id") REFERENCES "course"("cid") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "UNQ_class" UNIQUE("stitle","course_id","date","time"),
	PRIMARY KEY("sid" AUTOINCREMENT)
);
INSERT INTO "settings" ("detection_confidence","recogintion_threshold","image_per_student") VALUES (50,50,30);
INSERT INTO "student" ("uid","Sname") VALUES (2170003286,'Waleed'),
 (2170007761,'Omar');
INSERT INTO "attendence" ("aid","a_stu_id","a_class_id","status") VALUES (1,2170003286,1,1),
 (2,2170007761,1,0);
INSERT INTO "behavior" ("bid","b_class_id","b1%","b2%","b3%","b4%","b5%") VALUES (1,1,50.0,60.0,70.0,80.0,90.0);
INSERT INTO "user" ("username","Uname","email","password","type") VALUES ('abahasn','Abdulaziz Bahasan','abahasn@iau.edu.sa','0123456',1),
 ('amhussein','Aamir Mokhtar','amhussein@iau.edu.sa','0987654',0),
 ('kawlaqi','khalid Awlaqi','kawlaqi@iau.edu.sa','0456632',1);
INSERT INTO "student_photos" ("student_id","img_url") VALUES (2170003286,'file:///C:/Users/lenovo-pc/Desktop/IAU/GP 2020-2021/CS-511/Team Work/Charts/ER Diagram (SDS)/ERD all-Page-2.png'),
 (2170007761,'file:///C:/Users/lenovo-pc/Desktop/IAU/GP 2020-2021/CS-511/Team Work/Images/face-detection.png');
INSERT INTO "course" ("cid","code","ctitle") VALUES (1,'CS414','Computer Organization'),
 (2,'CS411','Software Engineering'),
 (3,'CS511','Project Proposal'),
 (4,'CIS423','Web-Based Systems');
INSERT INTO "class" ("sid","stitle","course_id","date","time","instructor") VALUES (1,'S7M1',2,'2020-10-11','08:00-10:00','abahasn'),
 (2,'S9M5',3,'2020-09-20','19:00-20:00','amhussein'),
 (3,'S8M2',4,'2020-03-15','10:00-12:00','abahasn'),
 (4,'S7M1',1,'2019-09-05','13:00-14:00','kawlaqi'),
 (5,'S7M1',3,'2020-10-10','09:00-10:00','amhussein'),
 (6,'S7M1',3,'2020-10-10','10:00-12:00','amhussein');
COMMIT;
