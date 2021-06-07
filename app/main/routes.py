import os
from flask import render_template, send_from_directory
from . import main

@main.route('/')
def index():
    return render_template('bot.html')

@main.route('/assets/<path:name>')
def get_asset(name):
    return send_from_directory('static', name)

@main.route('/meetings')
def get_meetings():
    return render_template('meetings.html')