from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, Response
from flask_mysqldb import MySQL, MySQLdb
from . import main
from .Forms import MessageForm
from datetime import datetime

mysql = MySQLdb.connect(host='localhost', user='root', passwd='mysql', db='awla_db')

# -------------------------------------------------------------------------+
# Application Management Section                                           |
# -------------------------------------------------------------------------+

@main.route("/applications")
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



@main.route("/search-apps", methods=['POST','GET'])
def search_apps():
    """search by application status"""
    if session['admin'] and request.method == "POST":
        if request.form.get('filter') == 'All':
            return show_apps()
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
    sql = "insert into comments(body, admin_email, applicant_email) values (%s, %s, %s)"
    values = [reason, session.get('email'), app]
    curs.execute(sql, values)
    mysql.commit()


@main.route("/process_apps", methods=['GET', 'POST'])
def process_apps():
    """ modify application data """
    if session['admin'] and request.method == "POST":
        # search by status: accepted, denied, status
        if "search-btn" in request.form:
            if request.form.get('filter') == 'All':
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

# -------------------------------------------------------------------------+
# Customer Support Respondent Section                                       |
# -------------------------------------------------------------------------+

@main.route('/comment-queue', methods=['POST', 'GET'])
def show_tickets():
    if session['admin']:
        curs = mysql.cursor()
        sql = """select id, status, question, requester, acceptor, time_created 
            from support_tickets order by time_created asc"""
        curs.execute(sql)
        tickets = []
        for row in curs:
            tickets.append(row)
        mysql.commit()
        if request.method == 'POST':
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


@main.route('/select-ticket/<ticket_id>', methods=['POST', 'GET'])
def select_ticket(ticket_id):
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

# -------------------------------------------------------------------------+
# Customer Support Respondent Section, Real Time Chat                      |
# -------------------------------------------------------------------------+

# in progress d/n delete 3/29
#def from_admin(ticket_id):
#    curs = mysql.cursor()
#    sql = 'select sender_email from support_messages where ticket_id = %s'
#    curs.execute(sql, [ticket_id])
#    emails = curs.fetchall()
#    mysql.commit()
#    sql = 'select admin from users where email = %s'
#    for x in emails:
#        new_str = str(x)
#        convert = new_str.strip("('',)")
#        test2 = curs.execute(sql, [convert])
#        if test2 == '0':
#            print(test2, 'false')
#            return False
#        else:
#            print(test2, 'true')
#            return True
        
def format_html(data):
    html = ""
    open_div = "<div class='cm-style'><div class='option-box'>"
    close_div = '</div></div>'
    div_open_plain = '<div>'
    div_close_plain = '</div>'
    count = 0
    for row in data:
        html += open_div
        for x in row:
            if isinstance(x, datetime):
                html += div_open_plain
                html += '<small>' + str(x) + '</small>'
                #if not from_admin(session.get('tkt')):
                html += """<div class='icons'>
                    <i class='fa fa-pencil-square' aria-hidden='true'> edit</i>
                    <i class='fa fa-trash' aria-hidden='true'> delete</i>
                </div>"""
                html += div_close_plain
            else:
                if count == 0:
                    html += div_open_plain
                count += 1
                html += "<p>" + x + "</p>"
                if count == 2:
                    html += div_close_plain
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

@main.route("/get-chat-log")
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

@main.route('/show-data')
def show_data():
    msg_data = get_data()
    data = format_html(msg_data)
    return data

# -------------------------------------------------------------------------+
# Customer Support Respondent Section, Ticket Actions                      |
# -------------------------------------------------------------------------+

@main.route('/message-action', methods=['POST'])
def message_action():
    if request.method == 'POST':
        curs = mysql.cursor()
        ticket_id = session.get('tkt')
        if 'take-ticket' in request.form:
            sql = "update support_tickets set status = %s, acceptor = %s where id = %s"
            values = ['taken', session.get('email'), ticket_id]
            print(values)
            curs.execute(sql, values)
            mysql.commit()
    return redirect(url_for('.select_ticket', ticket_id=ticket_id))

