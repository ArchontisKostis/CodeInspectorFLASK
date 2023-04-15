from flask import flash

from app.model.Analysis import Analysis
from app.model.Project import Project
from app.model.RepoDriller import RepoDriller
from app.model.RepoFile import RepoFile


class ProjectAnalyzer:
    def __init__(self, project_to_analyze: Project, repo_url):
        self.project = project_to_analyze
        self.repo_url = repo_url
        self.analysis = None
        self.repo_driller = None

    def initiate_analysis(self):
        self.analysis = Analysis(self.project)
        project_repo = self.project.repository

        self.repo_driller = RepoDriller(project_repo)

        commit_list = self.repo_driller.find_commits()
        self.project.set_commits(commit_list)

        if self.project.has_commits():
            project_name = self.repo_driller.find_project_name()
            self.analysis.set_project_name(project_name)

        else:
            flash('No commits found in the specified period. Using a larger Date Range could help.')

    def find_project_modified_files(self):
        repo_files = []
        modified_files = self.repo_driller.find_modified_files()
        for file in modified_files:
            repo_file = RepoFile(file.filename)
            repo_file.set_metric('CC', file.complexity)
            repo_file.set_metric('NLOC', file.nloc)
            repo_files.append(repo_file)
        self.project.set_modified_files(repo_files)

    def file_is_not_already_added(self, file):
        for curr_file in self.project.modified_files:
            if file.filename == curr_file.filename:
                return False
        return True

    def calculate_churn(self):
        commits = self.project.commits
        first_and_last_commit = self.repo_driller.find_first_and_last_commits(commits)
        from_hash = first_and_last_commit['first'].hash
        to_hash = first_and_last_commit['last'].hash

        # get the churn for all files
        all_files_churn = self.repo_driller.find_files_churn_avg(self.repo_url, from_hash, to_hash)

        # Filter to get only the java files
        java_files_churn = {}
        for file in all_files_churn:
            if '.java' in str(file):
                java_files_churn.update({file: all_files_churn[file]})

        # Parse the projects files and update the churn metric
        for repo_file in self.project.modified_files:
            for java_file in java_files_churn:
                if repo_file.name in java_file:
                    repo_file.set_metric('churn', java_files_churn[java_file])

        return java_files_churn


    def get_analysis(self):
        return self.analysis
