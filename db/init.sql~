
/*
* WARNING: Only run this script if you wish to create or recreate
* this project's database.
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
	created timestamp default current_timestamp
);

-- create admin user --------------------------------------------------------------------------
insert into users(fname, lname, email, password, ssn, dob, admin) values 
('admin', 'user', 'admin','asdf', '1234', curdate(), 'y');

-- create standard users ----------------------------------------------------------------------
insert into users(fname, lname, email, password, ssn, dob) values 
('Jesus', 'Smith', 'user1@gmail.com', 'asdf', '1111', curdate()),
('John', 'Johnson', 'user2@gmail.com', 'asdf', '1112', curdate()),
('Steve', 'Stevens', 'user3@gmail.com', 'asdf', '2224', curdate()),
('Firstname', 'Lastname', 'user4@gmail.com', 'asdf', '2225', curdate());


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
	created timestamp default current_timestamp,
	latitude DECIMAL(11,8) not null,
	longitude DECIMAL(11,8) not null,
	foreign key (applicant_email) references users(email)
);

-- create applications -------------------------------------------------------------------------
insert into applications
(applicant_email, fname, lname, language, zipcode, street, city, state, latitude, longitude) values 
('user1@gmail.com', 'Joe', 'Smith', 'English', '85002', '123 Streetname', 'Phoenix', 'AZ', 38.15291954103251, -97.11724379306288);


-- REPORTS SECTION -------------------------------------------------
create table reports (
	commentid int primary key not null auto_increment,
	reason varchar(40) not null,
	notes varchar(100) null,
	admin_email varchar(75) not null,
	applicant_email varchar(75) not null,
	time_changed timestamp default current_timestamp,
	foreign key (admin_email) references users(email),
	foreign key (applicant_email) references applications(applicant_email)
);

-- SUPPORT TICKETS & MESSAGES SECTION ----------------------------------------------------------
CREATE TABLE `support_tickets` (
  `id` int(11) primary key auto_increment NOT NULL,
  `question` varchar(75) NOT NULL,
  `requester` varchar(40) NOT NULL,
  `category` varchar(30) NOT NULL,
  `acceptor` varchar(40) DEFAULT NULL,
  `status` varchar(25) DEFAULT 'open',
  `time_created` timestamp default current_timestamp,
  foreign key (acceptor) references users(email)
);

CREATE TABLE `support_messages` (
  `id` int(11) primary key auto_increment NOT NULL,
  `sender_email` varchar(75) NOT NULL,
  `ticket_id` int(11) NOT NULL,
  `msg` varchar(100) NOT NULL,
  `time_submitted` timestamp default current_timestamp,
  foreign key (ticket_id) references support_tickets(id)
);

