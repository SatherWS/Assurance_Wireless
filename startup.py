from flask import Flask, render_template, request, redirect, url_for, session, Response
#from flask_mysqldb import MySQL, MySQLdb
from  geopy.geocoders import Nominatim
import itertools
from Forms import TicketForm
from passlib.hash import sha256_crypt
from datetime import datetime
import pymysql

app = Flask(__name__)
app.secret_key = "aknfn348h23h5rwainfoanfw4"
mysql = pymysql.connect(host='localhost', user='root', passwd='mysql', db='awla_db')
geolocator = Nominatim(user_agent="Assurance_Wireless")

# -------------------------------------------------------------------------+
# Customer Support Section                                                 |
# -------------------------------------------------------------------------+

@app.route('/new-ticket', methods=['POST', 'GET'])
def new_ticket():
    """ uses Forms.py to create ticket submission form """
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


@app.route('/submit-ticket')
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


@app.route('/messaging/<ticket_id>', methods=['POST', 'GET'])
def messenger(ticket_id):
    """ sends messages to AW admins """
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
    sql = """insert into applications(applicant_email, phone_number, fname, lname, 
    language, zipcode, street, city, state) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    if check_address(address_str):
        curs.execute(sql, app)
        mysql.commit()
    else:
        return "failed address does not exist"


# TODO: APPLY PASSWORD ENCRYPTION USING HASHLIB BEFORE ADDING TO DATABASE
@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Adds new entries to awla_db.user and awla.applications """
    if request.method == 'POST':
        # prepare insert statement -- users table
        fname = request.form['first']
        lname = request.form['last']
        email = request.form['email']
        password = request.form['password']
        #hashed_password = sha256_crypt.hash(password)  # Password is hashed (not in use)
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
            return redirect(url_for("home"))
        else:
            error = "failed address does not exist"
            return render_template("register.html", error=error)
    return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
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
                    return redirect(url_for("show_apps"))
                return redirect(url_for("show_status"))

        except TypeError as e:
            print("server error:", e)
            msg = "Error invalid credentials"
            return render_template("login.html", msg=msg)
        return render_template("login.html")


# Kills current user's session
@app.route("/logout")
def logout():
    session.clear()
    return render_template("home.html")

# -------------------------------------------------------------------------+
# Application Status Section                                               |
# -------------------------------------------------------------------------+

@app.route("/status")
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
 
@app.route("/")
def home():
    """ Load Homepage """
    return render_template("home.html")

@app.route("/map/")
def map():
    """ Stores landing page draft """
    return render_template("map.html")


@app.route("/contact/")
def contact():
    """ TODO: Describe project and leave developers contact information"""
    return render_template("contact.html")


# -----------------------------------------------------------------------------+
# Application Management Section                                               |
# -----------------------------------------------------------------------------+

@app.route("/applications")
def show_apps():
    """ shows all application data """
    if session['admin']:
        curs = mysql.cursor()
        sql = """select appid, status, fname, lname, 
        applicant_email, zipcode, created from applications"""
        curs.execute(sql)
        apps = []
        for row in curs:
            apps.append(row)
        mysql.commit()
    return render_template("admin_templates/applications.html", apps=apps)


@app.route("/search-apps", methods=['POST','GET'])
def search_apps():
    """search by application status"""
    if session['admin'] and request.method == "POST":
        curs = mysql.cursor()
        sql = """select appid, status, fname, lname, 
        applicant_email, zipcode, created from applications
        where status = %s"""
        value = [request.form.get('filter')]
        curs.execute(sql, value)
        mysql.commit()
        apps = []
        for row in curs:
            apps.append(row)
        return render_template("admin_templates/applications.html", apps=apps)


def app_comments(app, reason):
    """provide reason for accepting or denying applications"""
    curs = mysql.cursor()
    sql = "insert into reports(reasoning, admin_email, applicant_email) values (%s, %s, %s)"
    values = [reason, session.get('email'), app]
    curs.execute(sql, values)
    mysql.commit()  


@app.route("/process_apps", methods=['GET', 'POST'])
def process_apps():
    """ modify application data """
    if session['admin'] and request.method == "POST":
        # search by status: accepted, denied, status
        if "filter" in request.form:
            if request.form.get('filter') == 'Show All':
                return show_apps()
            else:
                return search_apps() 

        elif "submit_btn" in request.form:
            curs = mysql.cursor()
            apps = request.form.getlist("selected")
            # set status variable to value of accept or deny button
            status = request.form["submit_btn"]
            for i in apps:
                app_comments(i, request.form.get('reason'))
                sql = "update applications set status = %s where applicant_email = %s"
                values = (status, i)
                curs.execute(sql, values)
                mysql.commit()
            
            return show_apps()  # get results from modal then redirect view
        return render_template("admin_templates/applications.html")


# ----------------------------------------------------------------------------------+    
# Customer Support Ticket Responder Section                                         |
# ----------------------------------------------------------------------------------+

def filter_status():
    """ Filter by Ticket Status, function is similar to search_apps """
    if session['admin'] and request.method == 'POST':
        if 'tkt' in request.form:
            return show_tickets()
        curs = mysql.cursor()
        sql = """select id, status, category, question, requester, acceptor, time_created 
            from support_tickets where status = %s order by time_created asc"""
        values = [request.form.get('filter')]
        
        curs.execute(sql, values)
        mysql.commit()
        tickets = []
        for row in curs:
            tickets.append(row)
        return tickets


def filter_categories():
    curs = mysql.cursor()
    sql = """select id, status, category, question, requester, acceptor, time_created 
            from support_tickets where category = %s order by time_created asc"""
    values = [request.form.get('filter2')]
    curs.execute(sql, values)
    mysql.commit()
    tickets = []
    for row in curs:
        tickets.append(row)
    return tickets


@app.route('/comment-queue', methods=['POST', 'GET'])
def show_tickets():
    if session['admin']:
        curs = mysql.cursor()
        sql = """select id, status, category, question, requester, acceptor, time_created 
            from support_tickets order by time_created asc"""
        curs.execute(sql)
        tickets = []
        for row in curs:
            tickets.append(row)
        mysql.commit()

        if 'filter' in request.form and request.form['filter'] != 'Show All':
            tickets = filter_status()
        if 'filter2' in request.form:
            tickets = filter_categories()

        # move to ticket detail view if ticket is clicked
        if 'tkt' in request.form:
            ticket_id = request.form.get('tkt')
            return redirect(url_for('.select_ticket', ticket_id=ticket_id))
        return render_template('admin_templates/comment-queue.html', tickets=tickets)


def get_ticket_info(ticket_id):
    """ helper method for select_ticket(ticket_id) """
    curs = mysql.cursor()
    sql = 'select * from support_tickets where id = %s'
    curs.execute(sql, [ticket_id])
    rs = curs.fetchone()
    mysql.commit()
    return rs


@app.route('/select-ticket/<ticket_id>', methods=['POST', 'GET'])
def select_ticket(ticket_id):
    """ This function returns the admin's ticket response view and sends admin messages"""
    if session['admin']:
        curs = mysql.cursor()
        sender = session.get('email')
        session['tkt'] = ticket_id

        # add message to selected ticket
        if request.method == "POST":
            msg = request.form['msg']
            sql = """insert into support_messages 
                  (sender_email, ticket_id, msg) values (%s, %s, %s)"""
            values = [sender, ticket_id, msg]
            curs.execute(sql, values)

        mysql.commit()
        tkt_info = get_ticket_info(ticket_id)
        return render_template('admin_templates/ticket-response.html', tkt_info=tkt_info)


# ----------------------------------------------------------------------------------+
# Customer Support Respondent Section, Real Time Chat                               |
# ----------------------------------------------------------------------------------+

def format_html(data):
    html = ""
    open_div = "<div class='cm-style'><div class='option-box'>"
    close_div = '</div></div>'
    count = 0
    for row in data:
        html += open_div
        for x in row:
            if isinstance(x, datetime):
                html += '<div>'
                html += '<p>' + str(x) + '</p>'
                html += '</div>'
            else:
                if count == 0:
                    html += '<div>'
                count += 1
                html += '<p>' + x + '</p>'
                if count == 2:
                    html += '</div>'
        count = 0
        html += close_div
    return html

def get_data():
    curs = mysql.cursor()
    sql = """select sender_email, msg, time_submitted from support_messages 
    where ticket_id = %s order by time_submitted desc"""
    curs.execute(sql, [session.get('tkt')])
    mysql.commit()
    return curs.fetchall()

@app.route("/get-chat-log")
def get_chat_log():
    txt = get_data()
    formatted_txt =  'Customer Support Chat Log \nTime Recorded '+str(datetime.now()) + '\n'
    counter = len(txt)
    for row in txt:
        formatted_txt += '\nMessage #' + str(counter) + '\n'
        for x in row:
            if isinstance(x, datetime):
                formatted_txt += str(x) + '\n'
            else:    
                formatted_txt += x + '\n'
        counter -= 1
    return Response (formatted_txt, mimetype="text/txt", headers={"Content-disposition": "attachment; filename=chat-log.txt"})

@app.route('/show-data')
def show_data():
    msg_data = get_data()
    data = format_html(msg_data)
    return data


# ----------------------------------------------------------------------------------+
# Support Ticket Actions: accept ticket, change ticket status, remove               |
# ----------------------------------------------------------------------------------+

@app.route('/message-action', methods=['POST'])
def message_action():
    if request.method == 'POST' and session['admin']:
        curs = mysql.cursor()
        ticket_id = session.get('tkt')

        if 'mod-status' in request.form:
            print(request.form['mod-status'])
            sql = "update support_tickets set status = %s, acceptor = %s where id = %s"
            values = [request.form['mod-status'], session.get('email'), ticket_id]
            curs.execute(sql, values)
            mysql.commit()

        if 'delete-ticket' in request.form:
            sql = "delete from support_messages where ticket_id = %s"
            curs.execute(sql, [ticket_id])
            mysql.commit()
            sql = "delete from support_tickets where id = %s"
            curs.execute(sql, [ticket_id])
            mysql.commit()
            return redirect(url_for(".show_tickets"))
    return redirect(url_for('.select_ticket', ticket_id=ticket_id))

if __name__ == '__main__':
    app.debug=True
    app.run()
