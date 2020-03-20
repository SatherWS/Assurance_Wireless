from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from flask_socketio import SocketIO
from . import main
from . import AdminRoutes
from LifelineAssistant import createApp, socketio
import itertools
from .ChatForm import TicketForm, CommentForm

mysql = MySQLdb.connect(host='localhost', user='root', passwd='', db='awla_db')

@main.route('/new-ticket', methods=['POST', 'GET'])
def new_ticket():
    """ 1st form in the process creates a new ticket """
    form = CommentForm()
    if form.validate_on_submit():
        session['chat-email'] = form.contact.data
        session['ticket'] = form.title.data
        return redirect(url_for('.submit_ticket'))
    elif request.method == 'GET':
        form.contact.data = session.get('chat-email', '')
        form.title.data = session.get('ticket', '')
    return render_template("help_center/create-ticket.html", form=form)


@main.route('/submit-ticket')
def submit_ticket():
    """ Adds ticket to database redirects to comments section """
    client = session.get('chat-email')
    ticket = session.get('ticket')
    curs = mysql.cursor()
    sql = 'insert into support_tickets(title, requester) values (%s, %s)'
    values = [ticket, client]
    curs.execute(sql, values)
    mysql.commit()
    ticket_id = get_ticket_fk(ticket)
    return redirect(url_for('.messenger', ticket_id=ticket_id))


def get_ticket_fk(ticket):
    """
    Helper method for submit_ticket & start_messenger,
    gets the foreign key of new message
    """
    curs = mysql.cursor()
    sql = 'select distinct time_created, id from support_tickets where title = %s'
    curs.execute(sql, [ticket])
    rt = curs.fetchone()
    mysql.commit()
    return rt[1]


@main.route('/messaging/<ticket_id>', methods=['POST', 'GET'])
def messenger(ticket_id):
    curs = mysql.cursor()
    sender = session.get('chat-email')
    ticket = session.get('ticket')
    # add data related to given ticket
    if request.method == "POST":
        msg = request.form['msg']
        sql = "insert into support_messages (sender_email, ticket_id, msg) values (%s, %s, %s)"
        values = [sender, ticket_id, msg]
        curs.execute(sql, values)
    mysql.commit()
    # display data
    sql = "select * from support_messages where ticket_id = %s order by time_submitted desc"
    curs.execute(sql, [ticket_id])
    msgs = []
    for row in curs:
        msgs.append(row)
    mysql.commit()
    return render_template('help_center/comment.html', msgs=msgs)


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

        # TODO: IF SQL DATA INTEGRITY CONSTRAINT IS TRIGGERED AN ACCOUNT IS WRONGFULLY CREATED
        # inserts data into applications table
        sql = """insert into applications(applicant_email, phone_number, fname, lname, 
        language, zipcode, street, city, state) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (email, cell, fname, lname, language, zip_code, street, city, state)
        cur.execute(sql, values)
        mysql.commit()
        return redirect(url_for("main.home"))
    return render_template("register.html")


# TODO: ALLOW USERS TO MAKE MISTAKES WHEN ENTERING CREDENTIALS
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
                return redirect(url_for("main.show_apps"))
            return redirect(url_for("main.show_status"))
    else:
        return render_template("home.html")


# Kills current user's session
@main.route("/logout")
def logout():
    session.clear()
    return render_template("home.html")


# Displays application status for logged in customer
@main.route("/status")
def show_status():
    if session['email']:
        curs = mysql.cursor()
        # SQL join statement grabs user's dob from applications table
        sql = """select applications.fname, applications.lname, applications.created, applications.status, 
            applications.zipcode, applications.street, applications.city, applications.state, users.dob 
            from applications inner join users on applications.applicant_email = users.email
            where applicant_email = %s;"""
        user = session['email']
        curs.execute(sql, [user])
        data = curs.fetchall()
        rs = list(itertools.chain(*data))
    return render_template("status.html", rs=rs)


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



# LEGACY CODE FROM REAL-TIME CHAT FEATURE v
"""
To mess-around with this code's functionality navigate
to 127.0.0.1:5000/support 
"""
@main.route("/support", methods=['GET', 'POST'])
def support():
    """Login form to enter a room."""
    form = TicketForm()
    if form.validate_on_submit():
        session['nonuser_email'] = form.nonuser_email.data
        session['room'] = form.room.data
        return redirect(url_for('.create_ticket'))
    elif request.method == 'GET':
        form.nonuser_email.data = session.get('nonuser_email', '')
        form.room.data = session.get('room', '')
    return render_template("support.html", form=form)

@main.route('/create-ticket')
def create_ticket():
    room = session.get('room')
    user = session.get('nonuser_email')
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
    email = session.get('nonuser_email', '')
    room = session.get('nonuser_email', '')
    if email == '' or room == '':
        return redirect(url_for('.support'))
    return render_template('chat.html', email=email, room=room)
# END LEGACY CODE FROM REAL-TIME CHAT FEATURE ^


