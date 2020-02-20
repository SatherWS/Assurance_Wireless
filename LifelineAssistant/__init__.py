from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import re
from .views.sessionControl import sessionControl

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'awla_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = "aknfn348h23h5rwainfoanfw4"
mysql = MySQL(app)

# Registers external view control scripts
app.register_blueprint(sessionControl)

# Adds new entries to awla_db.user and awla.applications
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # prepare insert statement users table
        fname = request.form['first']
        lname = request.form['last']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['dob']
        ssn = request.form['ssn']
        cur = mysql.connection.cursor()
        
        # insert statement users table
        sql = "INSERT INTO users (fname, lname, email, password, ssn, dob) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (fname, lname, email, password, ssn, dob)
        cur.execute(sql, values)
        mysql.connection.commit()
        session['fname'] = fname
        session['lname'] = lname
        session['email'] = email

        # prepare insert statement applications table
        language = request.form.get('language')
        zip_code = request.form['zipcode']
        street = request.form['street']
        city = request.form['city']
        state = request.form.get('state') 
        cell = request.form['phone']

        # insert statement applications table
        sql = "INSERT INTO applications(applicant_email, phone_number, fname, lname, language, zipcode, street, city, state) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (email, cell, fname, lname, language, zip_code, street, city, state)
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

# Consider deleting below 2 views
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

# View functions for logged in customers and employees
@app.route("/admin_templates/accounts.html")
def accounts():
    return render_template("admin_templates/accounts.html")

@app.route("/admin_templates/applications.html")
def applications():
    return render_template("admin_templates/applications.html")

# Main method
if __name__ == "__main__":
    app.run(debug=True)
