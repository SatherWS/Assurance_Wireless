/*
* WARNING: Only run this script if you wish to wipe and/or recreate the current
* working database. DO NOT INCLUDE THIS FILE IN PRODUCTION.
*/
create database if not exists awla_db;
use awla_db;

-- remove existing data ------------------------------------------------------------------------
drop table if exists support_messages;
drop table if exists support_tickets;
drop table if exists comments;
drop table if exists applications;
drop table if exists users;

-- USERS SECTION -------------------------------------------------------------------------------
create table users (
	userid int primary key not null auto_increment,
	fname varchar(50),
	lname varchar(50),
	email varchar(75) unique not null,
	password varchar(25) not null,
	ssn char(4) not null,
	dob date not null,
	admin char(1) default 'n' not null,
	created datetime default current_timestamp
);

-- create admin user --------------------------------------------------------------------------
insert into users(fname, lname, email, password, ssn, dob, admin) values 
('admin', 'user', 'admin','asdf', '1234', curdate(), 'y');

-- create standard users ----------------------------------------------------------------------
insert into users(fname, lname, email, password, ssn, dob) values 
('Jesus', 'Smith', 'user1', 'asdf', '1111', curdate()),
('John', 'Johnson', 'user2', 'asdf', '1112', curdate()),
('Steve', 'Stevens', 'user3', 'asdf', '2224', curdate()),
('Firstname', 'Lastname', 'user4', 'asdf', '2225', curdate());

-- APPLICATIONS SECTION ------------------------------------------------------------------------
create table applications (
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

-- create applications -------------------------------------------------------------------------
insert into applications
(applicant_email, fname, lname, language, zipcode, street, city, state) values 
('user1', 'user1', 'smith', 'English', '85002', '123 Streetname', 'Phoenix', 'AZ'),
('user2', 'user2', 'Johnson', 'English', '85002', '124 Streetname', 'Phoenix', 'AZ'),
('user3', 'user3', 'Stevens', 'English', '85002', '125 Streetname', 'Phoenix', 'AZ'),
('user4', 'user4', 'Lastname', 'English', '85002', '126 Streetname', 'Phoenix', 'AZ');

-- COMMENTS SECTION [NOT IMPLEMENTED 3/26/2020] -------------------------------------------------
create table comments (
	commentid int primary key not null auto_increment,
	body varchar(40) not null,
	userid int not null,
	appid int not null,
	foreign key (userid) references users(userid),
	foreign key (appid) references applications(appid)
);

-- SUPPORT TICKETS & MESSAGES SECTION ----------------------------------------------------------
CREATE TABLE `support_tickets` (
  `id` int(11) primary key auto_increment NOT NULL,
  `question` varchar(75) NOT NULL,
  `requester` varchar(40) NOT NULL,
  `category` varchar(30) NOT NULL,
  `acceptor` varchar(40) DEFAULT NULL,
  `status` varchar(25) DEFAULT 'open',
  `time_created` datetime DEFAULT CURRENT_TIMESTAMP,
  foreign key (acceptor) references users(email)
);

CREATE TABLE `support_messages` (
  `id` int(11) primary key auto_increment NOT NULL,
  `sender_email` varchar(75) NOT NULL,
  `ticket_id` int(11) NOT NULL,
  `msg` varchar(100) NOT NULL,
  `time_submitted` datetime DEFAULT CURRENT_TIMESTAMP,
  foreign key (ticket_id) references support_tickets(id)
);


	
