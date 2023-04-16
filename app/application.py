import datetime
import traceback

from flask import Blueprint, render_template, request, flash
from git import GitCommandError
from pydriller import Repository
import plotly.express as plotx
from pydriller.repository import MalformedUrl

from app.model.Project import Project
from app.model.ProjectAnalyzer import ProjectAnalyzer

blueprint = Blueprint('application', __name__)


@blueprint.route('/', methods=('POST', 'GET'))
def index():
    filetypes = ['.java']

    try:
        if request.method == 'POST':
            repo_url = request.form['repo-url']
            from_date = request.form['from-date-input']
            to_date = request.form['to-date-input']

            # Create a repository based on wif we got any dates
            # If no dates were provided we will get the repo from the beginning
            if (from_date or to_date) == '':
                repo = Repository(
                    repo_url,
                    only_modifications_with_file_types=filetypes
                )
            else:
                repo = Repository(
                    repo_url,
                    since=datetime.datetime.strptime(from_date, '%Y-%m-%d'),
                    to=datetime.datetime.strptime(to_date, '%Y-%m-%d'),
                    only_modifications_with_file_types=filetypes
                )

            project_to_analyze = Project(repo)
            project_analyzer = ProjectAnalyzer(project_to_analyze, repo_url)

            project_analyzer.initiate_analysis()
            project_analyzer.find_project_modified_files()

            churn_dict = project_analyzer.calculate_churn()

            results = project_analyzer.get_analysis()
            project_files = project_to_analyze.modified_files

            plot_data = {'name': [point.get_name() for point in project_files],
                         'churn': [point.get_metric('churn') for point in project_files],
                         'cc': [point.get_metric('cc') for point in project_files]
                         }

            # Make Plotly figure
            fig = plotx.scatter(plot_data, x='churn', y='cc', hover_name='name')
            fig.update_layout(title=results.project_name)

            plot_html = fig.to_html(full_html=False)  # Convert the Plotly figure to an HTML string

            for file in churn_dict:
                print(f"Name: {file} | Churn: {churn_dict[file]}")

            flash('Analysis Complete', 'success')
            return render_template('results.html', analysis_results=results, plot_html=plot_html, repo_url=repo_url)

    except MalformedUrl as e:
        flash('The provided URL is not a git repository.', 'danger')
        traceback.print_exc()
    except GitCommandError as e:
        flash('Fatal Git Error. Make sure you provided a valid git repository url.', 'danger')
        traceback.print_exc()

    return render_template('index.html')
