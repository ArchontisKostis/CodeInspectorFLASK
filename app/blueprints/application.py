# Import the required external modules
from flask import Blueprint, render_template, request, flash, Request
from git import GitCommandError
from pydriller import Repository
from pydriller.repository import MalformedUrl

# Import functions and classes from other modules within the application
from app.blueprints import convert_string_to_date, parse_form_data, handle_exception
from app.model.Project import Project
from app.analysis.ProjectAnalyzer import ProjectAnalyzer
from app.plot.ScatterPlotCreator import ScatterPlotCreator

# Define a Flask blueprint for the web application
blueprint = Blueprint('application', __name__)


# Define a view function for the home page
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

            # Create a scatter plot of the analysis results
            scatter_plot_creator = ScatterPlotCreator(project_to_analyze)
            plot_html = scatter_plot_creator.create_html_plot(results.project_name)

            # Flash a success message and render the results template
            flash('Analysis Complete', 'success')
            return render_template('results.html', analysis_results=results, plot_html=plot_html, repo_url=repo_url)

    # Handle exceptions that may occur during the analysis
    except MalformedUrl as e:
        handle_exception('The provided URL is not a git repository.', 'danger')
    except GitCommandError as e:
        handle_exception('Fatal Git Error.', 'danger')

    # Render the index template
    return render_template('index.html')



