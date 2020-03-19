from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL, MySQLdb
from . import main

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
    if session['admin']:
        if request.method == "POST":
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

@main.route('/comment-queue')
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
        return render_template('admin_templates/comment-queue.html', tickets=tickets)


@main.route('/select-ticket', methods=['POST', 'GET'])
def select_ticket():
    if session['admin'] and request.method == 'POST':
        curs = mysql.cursor()
        ticket_id = request.form.get('tkt')
        session['ticket_id'] = ticket_id
        # displays data in responder's view
        sql = "select * from support_messages where ticket_id = %s"
        curs.execute(sql, [ticket_id])
        msgs = []
        for row in curs:
            msgs.append(row)
        mysql.commit()
        return render_template('admin_templates/ticket-response.html', msgs=msgs)


# TODO: INSERT ADMIN MESSAGES RELATED TO A TICKET
@main.route('/ticket-response')
def ticket_response():
    # add message data
    sql = "insert into support_messages (sender_email, ticket_id, msg) values (%s, %s, %s)"
    values = []
    pass

# Show all tickets in the queue -- OLD CHAT QUEUE FOR REAL-TIME MESSAGING D/N WORK
@main.route("/queue")
def chat_queue():
    if session['admin']:
        curs = mysql.cursor()
        sql = """select id, title, requester, acceptor, time_created 
            from tickets order by time_created asc"""
        curs.execute(sql)
        tickets = []
        for row in curs:
            tickets.append(row)
        mysql.commit()
    return render_template("admin_templates/queue.html", tickets=tickets)



