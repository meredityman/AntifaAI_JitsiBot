import os
from flask import render_template, send_from_directory
from . import main

@main.route('/')
def index():
    return render_template('bot.html')

