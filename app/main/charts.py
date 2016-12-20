from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm


@main.route('/charts/<suite>/<case>')
def charts(suite, case):
    print suite, case
    return render_template('charts.html', suite = suite, case = case)

@main.route('/ch/<suite>')
def ch(suite):
    print suite
    return render_template('ch.html', suite = suite)

