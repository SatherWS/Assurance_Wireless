from flask import Flask, render_template, request, redirect, url_for, session

def createApp(debug=False):
    _app = Flask(__name__)
    _app.debug = debug
    _app.secret_key = "aknfn348h23h5rwainfoanfw4"
    _app.config['TEMPLATES_AUTO_RELOAD'] = True
    from .main import main as main_blueprint
    _app.register_blueprint(main_blueprint)
    return _app





