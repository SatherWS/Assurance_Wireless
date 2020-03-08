from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from flask_socketio import SocketIO
from . import main
from . import AdminRoutes
from LifelineAssistant import createApp, socketio
import itertools
from .ChatForm import TicketForm


mysql = MySQLdb.connect(host='localhost', user='root', passwd='', db='awla_db')


# TODO/REFACTOR: SEPARATE INTO TWO METHODS
@main.route('/register', methods=['GET', 'POST'])
def register():
    """ Adds new entries to awla_db.user and awla.applications """
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # prepare insert statement -- users table
        fname = request.form['first']
        lname = request.form['last']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['dob']
        ssn = request.form['ssn']
        cur = mysql.cursor()

        # insert data into users table
        sql = """insert into users (fname, lname, email, 
        password, ssn, dob) VALUES (%s,%s,%s,%s,%s,%s)"""
        values = (fname, lname, email, password, ssn, dob)
        cur.execute(sql, values)
        mysql.commit()
        session['fname'] = fname
        session['lname'] = lname
        session['email'] = email

        # prepare insert statement -- applications table
        language = request.form.get('language')
        zip_code = request.form['zipcode']
        street = request.form['street']
        city = request.form['city']
        state = request.form.get('state')
        cell = request.form['phone']

        # TODO: IF SQL DATA INTEGRITY CONSTRAINT IS TRIGGERED ACCOUNT IS WRONGFULLY CREATED
        # inserts data into applications table
        sql = """insert into applications(applicant_email, phone_number, fname, lname, 
        language, zipcode, street, city, state) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (email, cell, fname, lname, language, zip_code, street, city, state)
        cur.execute(sql, values)
        mysql.commit()
        return redirect(url_for("main.home"))
    return render_template("register.html")


# User authentication function
@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == "POST":
        uname = request.form['username']
        password = request.form['password']
        cur = mysql.cursor()
        sql = "select * from users where email=%s AND password=%s"
        cur.execute(sql, (uname, password))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            session['email'] = user[3]
            if user[7] == 'y':
                session['admin'] = user[7]
                return redirect(url_for("main.showApps"))
            return redirect(url_for("main.showStatus"))
    else:
        return render_template("home.html")


# Kills current user's session
@main.route("/logout")
def logout():
    session.clear()
    return render_template("home.html")


# Displays application status for logged in customer
@main.route("/status")
def showStatus():
    if session['email']:
        curs = mysql.cursor()
        sql = """select applications.fname, applications.lname, applications.created, applications.status, applications.zipcode,
            applications.street, applications.city, applications.state, users.dob from applications 
            inner join users on applications.applicant_email = users.email
            where applicant_email = %s;"""
        user = session['email']
        curs.execute(sql, [user])
        data = curs.fetchall()
        rs = list(itertools.chain(*data))
    return render_template("status.html", rs=rs)


@main.route("/support", methods=['GET', 'POST'])
def support():
    """Login form to enter a room."""
    form = TicketForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['room'] = form.room.data
        return redirect(url_for('.createTicket'))
    elif request.method == 'GET':
        form.email.data = session.get('email', '')
        form.room.data = session.get('room', '')
    return render_template("support.html", form=form)


@main.route('/create-ticket')
def createTicket():
    room = session.get('room')
    user = session.get('email')
    curs = mysql.cursor()

    # SQL block adds ticket to db
    sql = "insert into tickets(title, requester) values (%s, %s)"
    values = [room, user]
    curs.execute(sql, values)
    mysql.commit()
    return redirect(url_for('.chat'))


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    email = session.get('email', '')
    room = session.get('room', '')
    if email == '' or room == '':
        return redirect(url_for('.support'))
    return render_template('chat.html', email=email, room=room)


# View functions for non logged in users
@main.route("/")
def home():
    return render_template("home.html")


# Stores landing page draft
@main.route("/about/")
def about():
    return render_template("about.html")


# Should contain team member info for potential employers
@main.route("/contact/")
def contact():
    return render_template("contact.html")



