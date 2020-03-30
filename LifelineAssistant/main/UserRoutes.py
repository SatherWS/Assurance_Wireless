from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from . import main
from . import AdminRoutes
from LifelineAssistant import createApp
import itertools
from .Forms import TicketForm

mysql = MySQLdb.connect(host='localhost', user='root', passwd='mysql', db='awla_db')

# -------------------------------------------------------------------------+
# Customer Support Section                                                 |
# -------------------------------------------------------------------------+

@main.route('/new-ticket', methods=['POST', 'GET'])
def new_ticket():
    """ 1st form in the process creates a new ticket """
    form = TicketForm()
    if form.validate_on_submit():
        session['chat-email'] = form.contact.data
        session['ticket'] = form.title.data
        session['category'] = form.category.data

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
    category = session.get('category')
    curs = mysql.cursor()
    sql = 'insert into support_tickets(question, requester, category) values (%s, %s, %s)'
    values = [ticket, client, category]
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
    sql = 'select distinct time_created, id from support_tickets where question = %s'
    curs.execute(sql, [ticket])
    rt = curs.fetchone()
    mysql.commit()
    return rt[1]


@main.route('/messaging/<ticket_id>', methods=['POST', 'GET'])
def messenger(ticket_id):
    curs = mysql.cursor()
    sender = session.get('chat-email')
    session['tkt'] = ticket_id
    # add message to selected ticket
    if request.method == "POST":
        msg = request.form['msg']
        sql = "insert into support_messages (sender_email, ticket_id, msg) values (%s, %s, %s)"
        values = [sender, ticket_id, msg]
        curs.execute(sql, values)
    mysql.commit()
    return render_template('help_center/comment.html')


# -------------------------------------------------------------------------+
# User Authentication Section                                              |
# -------------------------------------------------------------------------+

# TODO: APPLY PASSWORD ENCRYPTION USING HASHLIB BEFORE ADDING TO DATABASE
@main.route('/register', methods=['GET', 'POST'])
def register():
    """ Adds new entries to awla_db.user and awla.applications """
    if request.method == 'POST':
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
        values = [fname, lname, email, password, ssn, dob]
        cur.execute(sql, values)
        mysql.commit()
        session['email'] = email

        application = []  # pass list into add_application def
        application.append(request.form['email'])
        application.append(request.form['first'])
        application.append(request.form['last'])
        application.append(request.form.get('language'))
        application.append(request.form['phone'])
        application.append(request.form['street'])
        application.append(request.form['city'])
        application.append(request.form.get('state'))
        application.append(request.form['zipcode'])
        add_application(application)
        return redirect(url_for("main.home"))
    return render_template("register.html")


def add_application(app):
    curs = mysql.cursor()
    # use this string in find_coordinates.py
    """
    address_str = street+' '+city+ ' '+state+ ' '+zip_code
    print(address_str)  
    """
    # prepare insert statement -- applications table
    sql = """insert into applications(applicant_email, phone_number, fname, lname, 
    language, zipcode, street, city, state) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    curs.execute(sql, app)
    mysql.commit()


# TODO: ALLOW USERS TO MAKE MISTAKES WHEN ENTERING CREDENTIALS
# TODO: APPLY PASSWORD ENCRYPTION THROUGH HASHLIB BEFORE ADDING TO DATABASE
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

# -------------------------------------------------------------------------+
# Application Status Section                                               |
# -------------------------------------------------------------------------+

@main.route("/status")
def show_status():
    """ Displays application status for logged in customer """
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

# -------------------------------------------------------------------------+
# View Rendering Section                                                   |
# -------------------------------------------------------------------------+
 
@main.route("/")
def home():
    """ Load Homepage """
    return render_template("home.html")


@main.route("/map/")
def map():
    """ Stores landing page draft """
    return render_template("map.html")


@main.route("/contact/")
def contact():
    """ TODO: Describe project and leave developers contact information"""
    return render_template("contact.html")

