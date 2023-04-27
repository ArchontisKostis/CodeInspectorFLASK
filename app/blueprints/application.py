# Import the required external modules
import time

from flask import Blueprint, render_template, request, flash, Request, redirect, url_for, session
from git import GitCommandError
from pydriller import Repository
from pydriller.repository import MalformedUrl

# Import functions and classes from other modules within the application
from app.blueprints import convert_string_to_date, parse_form_data, handle_exception, calculate_time
from app.model.Project import Project
from app.analysis.ProjectAnalyzer import ProjectAnalyzer
from app.plot.ScatterPlotCreator import ScatterPlotCreator

# Define a Flask blueprint for the web application
blueprint = Blueprint('application', __name__)


# Define a view function for the home page
@blueprint.route('/', methods=('POST', 'GET'))
@blueprint.route('/home', methods=('POST', 'GET'))
def index():
    if request.method == 'POST':

        form_data = parse_form_data(request)
        repo_url = form_data['repo-url']
        from_date = form_data['from-date']
        to_date = form_data['to-date']

        # Save the repo url to session so other bp can have access
        session['repo_url'] = repo_url

        # Generate URLs for the analysis and results blueprints
        analyze_url = url_for('analysis.analyze', repo_url=repo_url, from_date=from_date, to_date=to_date)

        # Redirect to the analysis blueprint with the form data
        return redirect(analyze_url)

    # Render the index template
    return render_template('index.html')



