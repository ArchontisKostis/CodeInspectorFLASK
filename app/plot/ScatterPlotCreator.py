from app.model.Project import Project
import plotly.express as plotx

from app.plot import PRIORITY_COLORS


class ScatterPlotCreator:
    def __init__(self, project: Project):
        self.project = project
        self.project_files = project.modified_files
        self.plot_data = self.init_data()
        self.scatter_fig = None

    def init_data(self):
        plot_data = {
            'name': [point.get_name() for point in self.project_files],
            'churn': [point.get_metric('churn') for point in self.project_files],
            'complexity': [point.get_metric('cc') for point in self.project_files],
            'priority': [point.get_priority() for point in self.project_files]
        }
        return plot_data

    def create_scatter_plot_figure(self, title: str):
        fig = plotx.scatter(
            self.plot_data,
            x='churn', y='complexity',
            color='priority',
            hover_name='name',
            color_discrete_sequence=PRIORITY_COLORS
        )
        fig.update_layout(title=title)
        self.scatter_fig = fig

    def create_html_plot(self, title):
        if self.scatter_fig is None:
            self.create_scatter_plot_figure(title)
        return self.scatter_fig.to_html(full_html=False)