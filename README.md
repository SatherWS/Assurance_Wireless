

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

## Running the app 

1) **Run ampps.** Install it if you don't have it. No additional setup is required as long as it's installed on your computer.

2) In an integrated terminal or command prompt enter the following commands in the project's directory.
```
set FLASK_APP=LifelineAssistant 
set FLASK_DEBUG=1
flask run
````
