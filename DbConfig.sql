create database if not exists awla_db;
use awla_db;

-- Removes existing data
drop table if exists comments;
drop table if exists applications;
drop table if exists users;

-- Re-populates data
create table if not exists users (
	userid int primary key not null auto_increment,
	fname varchar(50),
	lname varchar(50),
	email varchar(75) unique not null,
	password varchar(25) not null,
	admin char(1) default 'n' not null,
	created datetime default current_timestamp
);

-- Adds non-admin user
/*
insert into users(fname, lname, email, password) values 
	('Test', 'Data', 'customer@asdf.com', 'asdf');
*/
	
-- Adds admin user
insert into users(fname, lname, email, password, admin) values 
('admin', 'user', 'admin@admin.com','asdf','y');


create table if not exists applications (
	appid int primary key not null auto_increment,
	applicant_email varchar(75) unique not null,
	fname varchar(50),
	lname varchar(50),
	language varchar(25) not null,
	zipcode varchar(20) not null,
	street varchar(100) not null,
	city varchar(30) not null,
	state varchar(30) not null,
	ssn varchar(20) unique not null,
	dob date not null,
	foreign key(applicant_email) references users(email)
);

/*
-- Insert application (used for testing)
INSERT INTO applications(applicant_email, fname,lname,language,zipcode,street,city,state,ssn,dob) 
VALUES ('customer@asdf.com', 'asdf','asdf','english','123455','road street','Atlantic City','nj','123443', '2020-10-10');
*/

create table if not exists comments (
	commentid int primary key not null auto_increment,
	body varchar(40) not null,
	userid int not null,
	appid int not null,
	foreign key (userid) references users(userid),
	foreign key (appid) references applications(appid)
);
	
