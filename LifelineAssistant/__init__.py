from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import re
import LifelineAssistant.sessionViews


app = Flask(__name__)
#app.register_blueprint(session_views)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'awla_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = "aknfn348h23h5rwainfoanfw4"
mysql = MySQL(app)

# Adds new entries to awla_db.user and awla.applications
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # insert data into users table
        fname = request.form['first']
        lname = request.form['last']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        
        # send statement 1
        sql = "INSERT INTO users (fname, lname, email, password) VALUES (%s,%s,%s,%s)"
        values = (fname, lname, email, password)
        cur.execute(sql, values)
        mysql.connection.commit()
        session['fname'] = fname
        session['lname'] = lname
        session['email'] = email

        # insert data into applications table
        language = request.form.get('language')
        zip_code = request.form['zipcode']
        street = request.form['street']
        city = request.form['city']
        state = request.form.get('state') 
        dob = request.form['dob']
        ssn = request.form['ssn']
        cell = request.form['phone']

        # send statement 2
        sql = "INSERT INTO applications(applicant_email, fname, lname, language, zipcode, street, city, state, ssn, dob) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (email, fname, lname, language, zip_code, street, city, state, ssn, dob)
        cur.execute(sql, values)
        mysql.connection.commit()
        return redirect(url_for("home"))
    return render_template("register.html")


# User authentication function
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

# Kills current user's session
@app.route("/logout")
def logout():
    session.clear()
    return render_template("home.html")

# View functions for non logged in users
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

# View functions for logged in customers and employees
"""
@app.route("/status/")
def status():
    return render_template("status.html")
"""

@app.route("/admin_templates/accounts.html")
def accounts():
    return render_template("admin_templates/accounts.html")

@app.route("/admin_templates/applications.html")
def applications():
    return render_template("admin_templates/applications.html")

# Main method
if __name__ == "__main__":
    app.run(debug=True)
