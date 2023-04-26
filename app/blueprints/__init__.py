import datetime
import traceback

from flask import Request, flash


def parse_form_data(request: Request):
    repo_url = request.form['repo-url']
    from_date = request.form['from-date-input']
    to_date = request.form['to-date-input']

    # If the dates are empty make them None
    if (from_date or to_date) == '':
        from_date = None
        to_date = None

    return {'repo-url': repo_url, 'from-date': from_date, 'to-date': to_date}


def convert_string_to_date(date_string: str):
    return datetime.datetime.strptime(date_string, '%Y-%m-%d')


def handle_exception(msg: str, alert_type: str):
    flash(msg, alert_type)
    traceback.print_exc()
