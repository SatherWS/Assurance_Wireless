# App Launching Point
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re


app = Flask(__name__)
app.run(debug = True) # allows code changes on refresh

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'awla_db'

# init mysql
mysql = MySQL(app)
#sess = session()

# TODO: Separate view renders from database functions
@app.route("/",methods=['GET', 'POST'])
def home():
    msg = []
    if request.method == "POST":
        fields = request.form
        uname = fields['username']
        password = fields['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM USERS WHERE EMAIL=%s AND PASSWORD=%s", (uname, password))
        mysql.connection.commit()
        ret = cur.fetchone()
        cur.close()

        if ret:
            session['loggedin'] = True
            session['id'] = ret['userid']
            session['username'] = ret['email']
            msg.append("Login Successs")
        else:
            msg.append("Login Failure")
    return render_template("home.html", msg=msg)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/status/")
def review():
    return render_template("status.html")

@app.route("/admin_templates/accounts.html")
def accounts():
    return render_template("admin_templates/accounts.html")

@app.route("/admin_templates/applications.html")
def applications():
    return render_template("admin_templates/applications.html")

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    #sess.init_app(app)

    app.debug = True
    app.run()
