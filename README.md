# Assurance Wireless Website Version 2.0
### A Lifeline Application Management & Support System 
This repository contains a rebuild of the current website https://www.assurancewireless.com/. The goals of this project is to improve Assurance Wireless's Lifeline application process by implementing the following features and services.

## Features & Related Functionalities 
### Revised Online Application
Our online application process differs from Assurance Wireless's current process by giving prospective customers the ability to monitor the status of their Lifeline application. The current system in place does not allow users to check when or if they will recieve free or discounted cellular services until after their application is accepted.

### Admin Console
The admin console is a feature that allows privileged users to review applications and answer questions in the customer support chat queue.

#### Use Cases
* Modifying Applications: Accepy, Deny
* View Applications: Filter by status, search distinct strings
* Modify user accounts (pending)
   * View located here `/Views/admin_templates/accounts.html`

### Customer Support Chat Room
This feature allows customers and potential customers alike to ask questions about anything related to Assurance Wireless's services.
A given customer creates a ticket based on a brief description of their problem and then an employee converses with the requester until a solution is determined.
All tickets and messages are saved in separate tables in the database `awla_db`

#### Feature's Use Case Table
| Actor | Use Case |
| --- | --- |
| Customer | Asks Question | 
| Employee | Responds to Question | 
| Employee | Views Chat Queue |
| Employee | Views Log File |

#### Bonus Feature: Virtual Assistant (bot)
* Research how to build a bot for the IRC channel. The bot will answer a few frequently asked questions by customers - *Medium Importance*

## Dependencies and Prerequisites
* Python version 3.0 or greater 
* Pip version 3.0 or greater
* Flask Web Framework

## Set Up
1. Clone or download this repository
2. Install flask using command `pip install flask`
3. Replace MySQL connection strings with your own credentials in the following lines
    * line 11 of `/LifelineAssistant/main/UserRoutes.py`
    * line 7 of `/LifelineAssistant/main/AdminRoutes.py`
    * line 6 of `/LifelineAssistant/main/ChatEvents.py`
```
mysql = MySQLdb.connect(host='localhost', user='YOUR-USERNAME', passwd='YOUR-PASSWORD', db='awla_db')
```

## Running the app 
1) **Run ampps.** Install it if you don't have it. No additional setup is required as long as it's installed on your computer.


