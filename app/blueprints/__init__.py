import datetime
import traceback

from flask import Request, flash


# Function to parse form data from a Flask request object
def parse_form_data(request: Request):
    # Extract repo URL, from-date, and to-date from the request object's form data
    repo_url = request.form['repo-url']
    from_date = request.form['from-date-input']
    to_date = request.form['to-date-input']

    # If the dates are empty make them None
    if (from_date or to_date) == '':
        from_date = None
        to_date = None

    # Return a dictionary with the parsed form data
    return {'repo-url': repo_url, 'from-date': from_date, 'to-date': to_date}


# Function to convert a string date to a datetime object
# We use it when we get the submitted data from the form
def convert_string_to_date(date_string: str):
    return datetime.datetime.strptime(date_string, '%Y-%m-%d')

# Function to handle exceptions
def handle_exception(msg: str, alert_type: str):
    flash(msg, alert_type)      # Flash a message to the user with the specified message and alert type
    traceback.print_exc()       # Print a stack trace of the exception that occurred
