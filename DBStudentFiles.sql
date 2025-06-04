CREATE DATABASE student_records; -- first creating the database 

CREATE TABLE IF NOT EXISTS students ( -- next creating the table for students info
	id INT PRIMARY KEY AUTO_INCREMENT, -- the id field is the primary key for ease of finding, auto increments based on the below number
    name VARCHAR(400) NOT NULL DEFAULT '', -- name field will have a variety of characters cannot be null the defualt is a blank string
    age INT NOT NULL DEFAULT 1, -- age field will be an integer not null default is just 1
    gender ENUM('M', 'F', 'O') NOT NULL, -- can only have these 3 fields: male, female, or other gender field cannot be left null
    major VARCHAR(40) NOT NULL DEFAULT '', -- student major can be anything variety of characters will be 40 as limit, cannot be null default is empty string
    phone VARCHAR(20) NOT NULL DEFAULT '' -- student phone number can be anything variety of characters will be 20 as limit, cannot be null default is emptry string
    ) AUTO_INCREMENT=700300001; -- this the auto increment student id number per project directions
    
CREATE TABLE IF NOT EXISTS passwords ( -- creating the passwords table
	username VARCHAR(15), -- username field max 15 characters
    password VARCHAR(15), -- password field max 15 characters
    id INT, -- the id is an integer
    FOREIGN KEY (id) REFERENCES students(id) -- student id is also foreign key referencing the students table so that when a new student is added it can be referenced here to create a link btw both tables
);

CREATE TABLE IF NOT EXISTS scores ( -- creating the scores table
    id INT NOT NULL, -- student id not null is an integer
    name VARCHAR(400) NOT NULL, -- name 400 character limit cannot be null
    cs1030 INT NOT NULL DEFAULT 0, -- class cannot be null default is 0 per projet directions
    cs1100 INT NOT NULL DEFAULT 0, -- class cannot be null default is 0 per projet directions
    cs2030 INT NOT NULL DEFAULT 0, -- class cannot be null default is 0 per projet directions
    PRIMARY KEY (id), -- primary key is the student id for ease of searching is unique id
    FOREIGN KEY (id) REFERENCES students(id) ON DELETE CASCADE -- foriegn key for the students table so a link is here btw both tables
);

INSERT INTO scores (id, name, cs1030, cs1100, cs2030) -- when I first created the code I forgot to include a fk or link to the tables so I had to manually enter these scores (fixed now)
VALUES ('700300003', 'Donald Trump', 0, 0, 0);

INSERT INTO scores (id, name, cs1030, cs1100, cs2030)
VALUES ('700300001', 'Joe Biden', 0, 0, 0);

INSERT INTO scores (id, name, cs1030, cs1100, cs2030)
VALUES ('700300004', 'Bill Gates', 0, 0, 0);

INSERT INTO scores (id, name, cs1030, cs1100, cs2030)
VALUES ('700300005', 'Elon Musk', 0, 0, 0);

INSERT INTO scores (id, name, cs1030, cs1100, cs2030)
VALUES ('700300006', 'Amber Veronese', 0, 0, 0);

INSERT INTO scores (id, name, cs1030, cs1100, cs2030)
VALUES ('700300007', 'Joseph Veronese', 0, 0, 0);

CREATE TRIGGER after_student_insert -- creating a trigger so that when a new student is created their info is automatically updated into the scores table so I dont have to manually update as I did above
AFTER INSERT ON students
FOR EACH ROW
INSERT INTO scores (id, name)  
VALUES (NEW.id, NEW.name);

ALTER TABLE passwords MODIFY password VARCHAR(32); -- when I created the hashed passwords I had to update the passsword table to include more characters than I originally had in code
