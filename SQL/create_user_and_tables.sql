create database novel;
use novel;

create user 'liguo'@'localhost' 
identified by "13212661081w";
grant alter,select,delete,update,insert,create,drop 
on novel.* 
to 'liguo'@'localhost';
create user 'spider'@'localhost' 
identified by "12345678";
grant select,delete,update,insert
on novel.* 
to 'spider'@'localhost';
flush privileges;

CREATE TABLE novel (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL,
    author_id INT NOT NULL,
    chapters_count INT,
    category_id INT,
    image_path VARCHAR(255),
    description VARCHAR(1024),
    last_update_date DATETIME,
    last_update_chapter INT,
    download_from VARCHAR(512),
    download_date DATETIME,
    download_finished char(1) default 'N',
    last_download_chapter INT,
    state varchar(30)
)  ENGINE=MYISAM CHARSET=UTF8;
       
CREATE TABLE chapter (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL,
    novel_id INT NOT NULL,
    serial INT NOT NULL,
    download_date DATETIME,
    word_count INT
)  ENGINE=MYISAM CHARSET=UTF8;

CREATE TABLE chapter_text (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    chapter_id int not null,
    text TEXT NOT NULL
)  ENGINE=MYISAM CHARSET=UTF8;

CREATE TABLE category_t (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    text VARCHAR(30),
    url VARCHAR(256),
    site VARCHAR(30)
)  ENGINE=MYISAM CHARSET=UTF8;

create table author (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(30),
    description varchar(1024)
) ENGINE=MYISAM CHARSET=UTF8;

create table download_result (
	id INT primary key not null auto_increment,
    url varchar(255),
    download_date datetime,
    result int
) ENGINE=MYISAM CHARSET=UTF8;

CREATE TABLE download_history (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    novel_id INT NOT NULL,
    last_chapter INT,
    url varchar(255),
    last_date DATETIME
)  ENGINE=MYISAM CHARSET=UTF8;