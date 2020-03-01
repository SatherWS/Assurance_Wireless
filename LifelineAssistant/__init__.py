from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from flask_socketio import SocketIO


socketio = SocketIO()


def createApp(debug=False):
    _app = Flask(__name__)
    _app.debug = debug
    _app.secret_key = "aknfn348h23h5rwainfoanfw4"

    from .main import main as main_blueprint
    _app.register_blueprint(main_blueprint)

    socketio.init_app(_app)
    return _app





