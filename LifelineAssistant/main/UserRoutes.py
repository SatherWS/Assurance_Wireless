from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from  geopy.geocoders import Nominatim
from . import main
from . import AdminRoutes
from LifelineAssistant import createApp
import itertools
from .Forms import TicketForm
from passlib.hash import sha256_crypt

#mysql = MySQLdb.connect(host='35.231.239.49', user='root', passwd='tGHC97h8xDoI6b1m', db='assurance-wireless-db')
mysql = MySQLdb.connect(host='localhost', user='root', passwd='mysql', db='awla_db')
geolocator = Nominatim(user_agent="Assurance_Wireless")

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
    return render_template('help_center/send-msg.html')


# -------------------------------------------------------------------------+
# User Authentication Section                                              |
# -------------------------------------------------------------------------+
def check_address(addr):
    location = geolocator.geocode(addr)
    try:
        print(location.address)
        print("GPS Coordinates",(location.latitude, location.longitude))
        return True

    except AttributeError:
        print("Location DNE")
        return False

def add_application(app):
    curs = mysql.cursor()
    address_str = app[6]+' '+app[8] +' '+app[5]
    # prepare insert statement -- applications table
    # email, phone, fname, lname, language, street, city, state, zipcode
    sql = """insert into applications(applicant_email, phone_number, fname, lname, 
    language, zipcode, street, city, state) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    if check_address(address_str):
        curs.execute(sql, app)
        mysql.commit()
    else:
        return "failed address does not exist"


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
        hashed_password = sha256_crypt.hash(password)  # Password is hashed (not in use)
        dob = request.form['dob']
        ssn = request.form['ssn']
        cur = mysql.cursor()

        # insert data into users table
        sql = """insert into users (fname, lname, email, 
        password, ssn, dob) VALUES (%s,%s,%s,%s,%s,%s)"""
        values = [fname, lname, email, password, ssn, dob]

        app = []  # pass list into add_application def
        app.append(request.form['email'])
        app.append(request.form['phone'])
        app.append(request.form['first'])
        app.append(request.form['last'])
        app.append(request.form.get('language'))
        app.append(request.form['zipcode'])
        app.append(request.form['street'])
        app.append(request.form['city'])
        app.append(request.form.get('state'))
        address_str = app[6]+' '+app[8] +' '+app[5]

        if check_address(address_str):
            cur.execute(sql, values)
            mysql.commit()
            session['email'] = email
            add_application(app)
            return redirect(url_for("main.home"))
        else:
            error = "failed address does not exist"
            return render_template("register.html", error=error)
    return render_template("register.html")


@main.route("/login", methods=['GET', 'POST'])
def login():
    """ working login method """
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
        try:  # if sql statement returns 1 row with 9 columns, continue
            if len(user) == 9:
                session['email'] = user[3]
                if user[7] == 'y':
                    session['admin'] = user[7]
                    return redirect(url_for("main.show_apps"))
                return redirect(url_for("main.show_status"))

        except TypeError as e:
            print("server error:", e)
            msg = "Error invalid credentials"
            return render_template("login.html", msg=msg)
        return render_template("login.html")


@main.route("/login-encrypted", methods=['GET', 'POST'])
def encrypted_login():
    """ In Progress Login Method """
    print(f"Logging in...")
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password_index = 4

        cursor = mysql.cursor()
        statement = "select * from users where email=%s" 
        cursor.execute(statement, [username])
        user = cursor.fetchone()
        cursor.close()

        if user is None:
            print(f"\tEntered email does not match our records.")
            flash("\n\nEntered email does not match our records.", "warning")
            return render_template("login.html")
        elif not sha256_crypt.verify(password, user[password_index]):
            print(f"\tEntered password was incorrect.")
            flash("\n\nEntered password was incorrect.", "error")
            return render_template("login.html")
        elif user is not None:
            session['email'] = user[3]
            if user[7] == 'y':
                session['admin'] = user[7]
                flash("Login successful!")
                return redirect(url_for("main.show_apps"))
            print(f"\tLogin successful!")
            flash("\n\nLogin successful!")
            return redirect(url_for("main.show_status"))
        else:
            print(f"\tUsername or password is incorrect!")
            flash("\n\nUsername or password is incorrect!", "warning")
            return render_template("login.html")
    else:
        print(F"Invalid...")
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
            where applicant_email = %s"""
        user = session['email']
        curs.execute(sql, [user])
        test = []
        for i in curs:
            test.append(i)
        print(test)
        data = curs.fetchall()
        rs = list(itertools.chain(*data))
        print(rs)
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

