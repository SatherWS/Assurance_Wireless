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
	ssn char(9) unique not null,
	dob date not null,
	admin char(1) default 'n' not null,
	created datetime default current_timestamp
);

-- create admin user
insert into users(fname, lname, email, password, ssn, dob, admin) values 
('admin', 'user', 'admin','asdf', '123412344', curdate(), 'y');

-- create standard users
insert into users(fname, lname, email, password, ssn, dob) values 
('user1', 'smith', 'user1', 'asdf', '111122222', curdate()),
('user2', 'Johnson', 'user2', 'asdf', '111122223', curdate()),
('user3', 'Stevens', 'user3', 'asdf', '111122224', curdate()),
('user4', 'Lastname', 'user4', 'asdf', '111122225', curdate());

create table if not exists applications (
	appid int primary key not null auto_increment,
	applicant_email varchar(75) not null,
	phone_number varchar(20) null,
	status varchar(25) default 'Pending' not null,
	fname varchar(50),
	lname varchar(50),
	language varchar(25) not null,
	zipcode varchar(20) not null,
	street varchar(100) not null,
	city varchar(30) not null,
	state varchar(30) not null,
	created datetime default current_timestamp,
	foreign key(applicant_email) references users(email)
);

-- create applications
insert into applications
(applicant_email, fname, lname, language, zipcode, street, city, state) values 
('user1', 'user1', 'smith', 'English', '85002', '123 Streetname', 'Phoenix', 'AZ'),
('user2', 'user2', 'Johnson', 'English', '85002', '124 Streetname', 'Phoenix', 'AZ'),
('user3', 'user3', 'Stevens', 'English', '85002', '125 Streetname', 'Phoenix', 'AZ'),
('user4', 'user4', 'Lastname', 'English', '85002', '126 Streetname', 'Phoenix', 'AZ');


create table if not exists comments (
	commentid int primary key not null auto_increment,
	body varchar(40) not null,
	userid int not null,
	appid int not null,
	foreign key (userid) references users(userid),
	foreign key (appid) references applications(appid)
);
	
