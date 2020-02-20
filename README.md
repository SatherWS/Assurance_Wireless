# Lifeline Application Management & Support System 
This repository contains a hypothetical web application for Assurance Wireless. This project's goal is to improve Assurance Wireless's Lifeline application process. This project was written using Visual Studio Code IDE. Other text editors like PyCharm could work aswell.

## Dependencies and Prerequisites
* Python version 3.0 or greater 
* Pip version 3.0 or greater
* Flask Web Framework

## Set Up
1. Clone or download this repository
2. Install flask using command `pip install flask`
3. Configure database in mysql shell with command `source C:/path/to/Assurance_Wireless/DbConfig.sql`
4. Replace lines 11 and 12 of `/LifelineAssistant/__init__.py` with your own mysql credentials
```
app.config['MYSQL_USER'] = '<your username>'
app.config['MYSQL_PASSWORD'] = '<your password>'
```
5. Replace line 8 of `/LifelineAssistant/views/sessionView.py` with your own mysql credentials
```
mysql = MySQLdb.connect(host='localhost', user='YOUR-USERNAME', passwd='YOUR-PASSWORD', db='awla_db')
```

## Running the app in development mode
In an integrated terminal or command prompt enter the following commands in the project's directory.
```
set FLASK_APP=LifelineAssistant 
set FLASK_DEBUG=1
flask run
````

## Problems to Solve: 
### Web App Functions / UI Tools
* Build admin panel for accepting/denying customer applications (In Progress)
* Build admin tool for managing customers (Not Started)
  * View located here `/Views/admin_templates/accounts.html`
 
 ### Fraud Prevention / Data Integrity 
 * Use Email Validation API to prevent users from entering non-existent email addresses - *High Importantce*
   * https://pypi.org/project/email-verifier/
 * Mimic existing zip code API to generate the city and state that belongs to an inputed zip code - *Medium Importance* 

### IRC Chat & Virtual Assistant
* Research how to integrate a chat room component to the project - *High Importance*
* Research how to build a bot for the IRC channel. The bot will answer a few general questions - *Medium Importance*
