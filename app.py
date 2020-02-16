# App Launching Point
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from flask_login import LoginManager #not in use
#from flask_session import Session
import re


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'awla_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = "aknfn348h23h5rwainfoanfw4"
mysql = MySQL(app)

# User authentication and creation functions
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        fname = request.form['first']
        lname = request.form['last']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (fname, lname, email, password) VALUES (%s,%s,%s,%s)",
        (fname, lname, email, password))
        cur.execute("INSERT INTO applications(")
        mysql.connection.commit()
        session['fname'] = fname
        session['lname'] = lname
        session['email'] = email
        return redirect(url_for("home"))


@app.route("/login",methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        uname = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM USERS WHERE EMAIL=%s AND PASSWORD=%s", (uname, password))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            session['email'] = user['email']
            if user['admin'] == 'y': session['admin'] = user['admin']
            return render_template("home.html")
        else:
            return "Invalid email and password"
    else:
        return render_template("home.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("home.html")

# View functions
@app.route("/")
def home():
    return render_template("home.html")

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
    app.run(debug=True)
