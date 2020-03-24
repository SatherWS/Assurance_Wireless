from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL, MySQLdb
from . import main
from .ChatForm import MessageForm

mysql = MySQLdb.connect(host='localhost', user='root', passwd='', db='awla_db')

# Shows data in application management view
@main.route("/applications")
def show_apps():
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

# Modify application status
@main.route("/process_apps", methods=['GET', 'POST'])
def process_apps():
    if session['admin'] and request.method == "POST":
        if "search-btn" in request.form:
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

        # TODO: POSSIBLY SEPARATE THIS FUNCTION
        elif "submit_btn" in request.form:
            curs = mysql.cursor()
            apps = request.form.getlist("selected[]")
            # set status variable to value of accept or deny button
            status = request.form["submit_btn"]
            for i in apps:
                sql = "update applications set status = %s where appid = %s"
                values = (status, i)
                curs.execute(sql, values)
                mysql.commit()
            return show_apps()
        return render_template("admin_templates/applications.html")

@main.route('/comment-queue', methods=['POST', 'GET'])
def show_tickets():
    if session['admin']:
        curs = mysql.cursor()
        sql = """select id, title, requester, acceptor, time_created 
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
        # add message to selected ticket
        if request.method == "POST":
            msg = request.form['msg']
            sql = "insert into support_messages (sender_email, ticket_id, msg) values (%s, %s, %s)"
            values = [sender, ticket_id, msg]
            curs.execute(sql, values)
        mysql.commit()
        # displays messages in employee responder's viewS
        sql = "select * from support_messages where ticket_id = %s order by time_submitted desc"
        curs.execute(sql, [ticket_id])
        msgs = []
        for row in curs:
            msgs.append(row)
        mysql.commit()

        tkt_info = get_ticket_info(ticket_id)
        return render_template('admin_templates/ticket-response.html', msgs=msgs, tkt_info=tkt_info)



