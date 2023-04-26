import datetime
import traceback

from flask import Blueprint, render_template, request, flash, Request
from git import GitCommandError
from pydriller import Repository
from pydriller.repository import MalformedUrl

from app.blueprints import convert_string_to_date, parse_form_data, handle_exception
from app.model.Project import Project
from app.analysis.ProjectAnalyzer import ProjectAnalyzer
from app.plot.ScatterPlotCreator import ScatterPlotCreator

blueprint = Blueprint('application', __name__)


@blueprint.route('/', methods=('POST', 'GET'))
def index():
    filetypes = ['.java']

    try:
        if request.method == 'POST':
            form_data = parse_form_data(request)
            repo_url = form_data['repo-url']
            from_date = form_data['from-date']
            to_date = form_data['to-date']

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

            project_to_analyze = Project(repo)
            project_analyzer = ProjectAnalyzer(project_to_analyze, repo_url)

            project_analyzer.initiate_analysis()
            project_analyzer.find_project_modified_files()

            project_analyzer.calculate_churn()

            project_analyzer.prioritize_hotspots()
            results = project_analyzer.get_analysis()

            scatter_plot_creator = ScatterPlotCreator(project_to_analyze)
            plot_html = scatter_plot_creator.create_html_plot(results.project_name)

            flash('Analysis Complete', 'success')
            return render_template('results.html', analysis_results=results, plot_html=plot_html, repo_url=repo_url)

    except MalformedUrl as e:
        handle_exception('The provided URL is not a git repository.', 'danger')
    except GitCommandError as e:
        handle_exception('Fatal Git Error.', 'danger')

    return render_template('index.html')



