# Assurance Wireless Website Version 2.0
### A Lifeline Application Management & Support System 
This repository contains a rebuild of the current website https://www.assurancewireless.com/. The goals of this project is to improve Assurance Wireless's Lifeline application process by implementing the following features and services.


## Features & Related Functionalities 
### Revised Online Application Process
Our online application process differs from Assurance Wireless's current process by giving prospective customers the ability to monitor the status of their Lifeline application. The current system in place does not allow users to check when or if they will recieve free or discounted cellular services until after their application is accepted.


### Admin Views: Application Management Console and Customer Support Queue
The admin console is a feature that allows privileged users to review applications and answer questions in the customer support chat queue.


### Customer Support Chat Room
This feature allows customers and potential customers alike to ask questions about anything related to Assurance Wireless's services.
A given customer creates a ticket based on a brief description of their problem and then an employee converses with the requester until a solution is determined.
All tickets and messages are saved in separate tables in the database `awla_db`


#### Bonus Feature: Customer Support Bot
* The bot will answer a few frequently asked questions by customers, TBD if it will be implemented

## Dependencies and Prerequisites
* Python version 3.0 or greater 
* Pip version 3.0 or greater
* Flask Web Framework

## Set Up
1. Clone or download this repository
2. Install flask using command `pip install flask`
3. Replace MySQL connection strings with your own credentials in UserRoutes.py and AdminRoutes.py

```
mysql = MySQLdb.connect(host='localhost', user='YOUR-USERNAME', passwd='YOUR-PASSWORD', db='awla_db')
```

## Running the app 
1) **Run ampps.** Install it if you don't have it. No additional setup is required as long as it's installed on your computer.
2) **Setup Database** in mysql shell with command `source C:/path/to/Assurance_Wireless/DbConfig.sql`. If you skip this step the project will crash.
3) **Run startup.py** This script is the launching point of the entire application

