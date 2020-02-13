# Assurance Wireless
Capstone project for software engineering class

## Dependencies and Prerequisites
* Python version 3.0 or greater 
* Flask Web Framework
* Pip version 3.0 or greater
* Microsoft Azure account (free for one year)
https://azure.microsoft.com/en-us/

## Project Set Up
Install flask using pip
pip install flask

### Database Set Up
mysql -u <username> -p
source /path/to/DbConfig.sql

Change lines 11 and 12 of app.py to
app.config['MYSQL_USER'] = '<your username>'
app.config['MYSQL_PASSWORD'] = '<your password'

Bot Configuration


Running the app in development mode
set FLASK_APP=app.py 
set FLASK_DEBUG=1
flask run

Directory & Scripts Descriptions




