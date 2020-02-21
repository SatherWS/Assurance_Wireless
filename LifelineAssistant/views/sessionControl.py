from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL, MySQLdb
import re
import itertools
#import dbConnection as db

sessionControl = Blueprint('sessionControl', __name__, template_folder='templates')
mysql = MySQLdb.connect(host='localhost', user='root', passwd='', db='awla_db')


# Displays application status for logged in customer
@sessionControl.route("/status")
def showStatus():
    if session['email']:
        curs = mysql.cursor() 
        sql = "select fname, lname, created, status, zipcode, street, city, state from applications where applicant_email = %s"
        user = session['email']
        curs.execute(sql, [user])
        data = curs.fetchall()
        rs = list(itertools.chain(*data))
    return render_template("status.html", rs=rs)


# Shows data in application management view
@sessionControl.route("/applications")
def showApps():
    if session['admin']:
        curs = mysql.cursor()
        sql = "select appid, status, fname, lname, applicant_email, zipcode, created from applications"
        curs.execute(sql)
        apps = []
        for row in curs:
            apps.append(row)
    return render_template("admin_templates/applications.html", apps=apps)


# Modify application status
@sessionControl.route("/updateApps", methods=['GET', 'POST'])
def updateApps():
    if request.post == "POST":
        return "test"
        
    return render_template("admin_templates/applications.html")
