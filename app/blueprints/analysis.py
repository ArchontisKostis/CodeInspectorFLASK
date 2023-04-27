import time

from flask import Blueprint, session, url_for, redirect
from git import GitCommandError
from pydriller import Repository
from pydriller.repository import MalformedUrl

from app.analysis.ProjectAnalyzer import ProjectAnalyzer
from app.blueprints import convert_string_to_date, handle_exception, calculate_time
from app.blueprints.results import display_results
from app.model.Project import Project

analysis_bp = Blueprint('analysis', __name__)

# Define a view function for the analysis
@analysis_bp.route('/analyze/', defaults={'from_date': None, 'to_date': None}, methods=('GET',))
@analysis_bp.route('/analyze/<from_date>/<to_date>', methods=('GET',))
def analyze(from_date, to_date):
    filetypes = ['.java']
    repo_url = session.get('repo_url')
    try:
        # start calculating how long it takes
        start_time = time.time()

        # Create a repository based on wif we got any dates
        # If no dates were provided we will get the repo from the beginning
        if not (from_date or to_date):
            repo = Repository(repo_url, only_modifications_with_file_types=filetypes)
        else:
            since = convert_string_to_date(from_date)
            to = convert_string_to_date(to_date)
            repo = Repository(
                repo_url, since=since, to=to,
                only_modifications_with_file_types=filetypes
            )

        # Create a Project object based on the repository
        project_to_analyze = Project(repo)

        # Create a ProjectAnalyzer object based on the Project and the repository URL and initiate analysis
        project_analyzer = ProjectAnalyzer(project_to_analyze, repo_url)
        project_analyzer.initiate_analysis()

        # Find the files in the project that have been modified during the specified date range (if any)
        project_analyzer.find_project_modified_files()

        # Calculate the churn (number of modifications) for each file in the project
        project_analyzer.calculate_churn()

        # Prioritize the files based on their churn and complexity
        project_analyzer.prioritize_hotspots()

        # Get the results of the analysis
        results = project_analyzer.get_analysis()

        # Store the analysis results and repo url in the session variable
        # session['analysis_results'] = results
        # session['repo_url'] = repo_url

        calculate_time(start_time)
        # Create results url and redirect
        results_url = url_for('results.display_results', results=results, repo_url=repo_url)
        return display_results(results, repo_url)

    # Handle exceptions that may occur during the analysis
    except MalformedUrl as e:
        handle_exception('The provided URL is not a git repository.', 'danger')
    except GitCommandError as e:
        handle_exception('Fatal Git Error.', 'danger')