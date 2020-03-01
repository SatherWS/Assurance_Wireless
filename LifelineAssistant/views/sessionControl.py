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
        sql = """select fname, lname, created, status, zipcode,
         street, city, state from applications where applicant_email = %s"""
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
        sql = """select appid, status, fname, lname, 
        applicant_email, zipcode, created from applications"""
        curs.execute(sql)
        apps = []
        for row in curs:
            apps.append(row)
    return render_template("admin_templates/applications.html", apps=apps)


# Modify application status
@sessionControl.route("/processApps", methods=['GET', 'POST'])
def processApps():
    if request.method == "POST":
        if "search-btn" in request.form:
            if request.form.get('filter') == 'All':
                return showApps()
            curs = mysql.cursor()
            sql = """select appid, status, fname, lname, 
            applicant_email, zipcode, created from applications
            where status = %s"""
            value = [request.form.get('filter')]
            curs.execute(sql, value)
            apps = []
            for row in curs:
                apps.append(row)
            return render_template("admin_templates/applications.html", apps=apps)
            
        elif "submit_btn" in request.form:
            curs = mysql.cursor()
            apps = request.form.getlist("selected")
            status = request.form["submit_btn"]
            for i in apps:
                sql = "update applications set status = %s where appid = %s"
                values = (status, i)
                curs.execute(sql, values)
                mysql.commit()
            return showApps()
    return render_template("admin_templates/applications.html")

