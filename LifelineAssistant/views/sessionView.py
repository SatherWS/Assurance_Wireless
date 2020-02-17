from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL, MySQLdb
import re
import itertools
#import dbConnection as db

sessionView = Blueprint('sessionView', __name__, template_folder='templates')
mysql = MySQLdb.connect(host='localhost', user='root', passwd='', db='awla_db')

@sessionView.route("/status")
def showStatus():
    if session['email']:
        curs = mysql.cursor() 
        sql = "SELECT fname, lname, created, status, zipcode, street, city, state FROM applications WHERE applicant_email = %s"
        user = session['email']
        curs.execute(sql, [user])
        data = curs.fetchall()
        rs = list(itertools.chain(*data))
    return render_template("status.html", rs=rs)