from flask import Blueprint, session, render_template, flash

from app.plot.ScatterPlotCreator import ScatterPlotCreator

results_bp = Blueprint('results', __name__)

# Define a view function for the results
@results_bp.route('/results/', methods=('GET',))
def display_results():
    # Get the analysis results from the session variable
    results = session.get('analysis_results', None)
    repo_url = session.get('repo_url', None)

    # Helper Variables
    analyzed_project = results.project
    project_name = results.project_name

    # Create a scatter plot of the analysis results
    scatter_plot_creator = ScatterPlotCreator(analyzed_project)
    plot_html = scatter_plot_creator.create_html_plot(project_name)

    # Flash a success message and render the results template
    flash('Analysis Complete', 'success')

    # Render the results template
    return render_template('results.html', analysis_results=results, plot_html=plot_html, repo_url=repo_url)