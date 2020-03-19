# NOT IN USE SINCE REAL-TIME CHAT API ISN'T WORKING

from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from flask_mysqldb import MySQLdb

mysql = MySQLdb.connect(host='localhost', user='root', passwd='', db='awla_db')


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    user = session.get('nonuser_email')
    admin = session.get('email')
    join_room(room)
    if user:
        emit('status', {'msg': user + ' has entered the room.'}, room=room)
    if admin:
        emit('status', {'msg': admin + ' has entered the room.'}, room=room)


# TODO/REFACTOR: SEPARATE INTO TWO METHODS
@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    user = session.get('nonuser_email')
    admin = session.get('email')
    curs = mysql.cursor()

    # SQL block finds message's foreign key for it's related ticket
    sql = "select (id) from tickets where title = %s"
    curs.execute(sql, [room])
    ticket_id = curs.fetchone()
    mysql.commit()

    if admin:
        # SQL block adds messages to db with ticket foreign key
        sql = "insert into messages(client_email, msg, ticket_id) values (%s, %s, %s)"
        values = [admin, message, ticket_id]
        curs.execute(sql, values)
        mysql.commit()
        emit('message', {'msg': admin + ':' + message['msg']}, room=room)
    elif user:
        # SQL block adds messages to db with ticket foreign key
        sql = "insert into messages(client_email, msg, ticket_id) values (%s, %s, %s)"
        values = [user, message, ticket_id]
        curs.execute(sql, values)
        mysql.commit()
        emit('message', {'msg': user + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('nonuser_email') + ' has left the room.'}, room=room)


# TODO: WRITE JOIN TICKET METHOD TO BE USED BY ADMINS
"""
@socketio.on('select', namespace='/chat')
def join_chat():
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has joined the room.'}, room=room)
"""

