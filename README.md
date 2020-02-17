# Lifeline Application Management System 
This repository contains a hypothetical web application for Assurance Wireless. This project's goal is to improve Assurance Wireless's Lifeline application process. This project was written using Visual Studio Code IDE. Other text editors like PyCharm could work aswell.

## Dependencies and Prerequisites
* Python version 3.0 or greater 
* Pip version 3.0 or greater
* Flask Web Framework
* Microsoft Bot Framework (see below link) <br/>
https://docs.microsoft.com/en-us/azure/bot-service/python/bot-builder-python-quickstart?view=azure-bot-service-4.0

## Set Up
1. Clone or dowload this repository
2. Install flask using command `pip install flask`
3. Configure database in mysql shell with command `source C:/path/to/Assurance_Wireless/DbConfig.sql`
4. Replace lines 11 and 12 of app.py with your own mysql credentials
```
app.config['MYSQL_USER'] = '<your username>'
app.config['MYSQL_PASSWORD'] = '<your password>'
```

## Running the app in development mode
In an integrated terminal or command prompt enter the following commands in the project's directory.
* set FLASK_APP=app.py 
* set FLASK_DEBUG=1
* flask run

## TODO: 2/16/2020
* Build admin panel for accepting/denying customer applications
* Implement 'Application Status' button
  * create application status view
