from app.model.Project import Project


class Analysis:
    def __init__(self, project: Project):
        self.project_name = 'Undefined Project Name'
        self.project = project

    def set_project_name(self, name):
        self.project_name = name