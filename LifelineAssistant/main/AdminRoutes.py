from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL, MySQLdb
from . import main


sessionControl = Blueprint('sessionControl', __name__, template_folder='templates')
mysql = MySQLdb.connect(host='localhost', user='root', passwd='', db='awla_db')


# Shows data in application management view
@main.route("/applications")
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
@main.route("/processApps", methods=['GET', 'POST'])
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
            # set status variable to value of accept or deny button
            status = request.form["submit_btn"]
            for i in apps:
                sql = "update applications set status = %s where appid = %s"
                values = (status, i)
                curs.execute(sql, values)
                mysql.commit()
            return showApps()
    return render_template("admin_templates/applications.html")

