from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import re
from flask.blueprints import Blueprint
#from LifelineAssistant import app

session_views = Blueprint('session_views', __name__, template_folder='templates')

@session_views.route("/status/")
def showStatus():
    return render_template("status.html")