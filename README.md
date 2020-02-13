# Lifeline Application Management Software for Assurance Wireless 
Capstone project for software engineering class

## Dependencies and Prerequisites
* Python version 3.0 or greater 
* Pip version 3.0 or greater
* Flask Web Framework
* Microsoft Azure account (to use bot framework)
https://azure.microsoft.com/en-us/

## How to Install
1. Clone or dowload this repository
2. Install flask using command `pip install flask`
3. Configure database in mysql shell with command `source C:/path/to/Assurance_Wireless/DbConfig.sql`
4. Change lines 11 and 12 of app.py to...
app.config['MYSQL_USER'] = '<your username>'
app.config['MYSQL_PASSWORD'] = '<your password'

Bot Configuration


Running the app in development mode
set FLASK_APP=app.py 
set FLASK_DEBUG=1
flask run

Directory & Scripts Descriptions




