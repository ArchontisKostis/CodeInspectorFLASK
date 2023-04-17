from app.model.PriorityType import PriorityType


class RepoFile:
    def __init__(self, name: str):
        self.name = name
        self.metrics = {'CC': -1, 'NLOC': -1, 'CHURN': -1}
        self.priority = 'NOT SET'

    def set_metric(self, metric_key: str, metric_value: int):
        key = str.upper(metric_key)
        self.metrics[key] = metric_value

    def get_name(self):
        return self.name

    def get_metric(self, metric_key: str) -> int:
        key = str.upper(metric_key)
        return self.metrics[key]

    def get_all_metrics(self) -> dict:
        return self.metrics

    def set_priority(self, type):
        print(self.name)
        print(f'RepoFile -> Priority To add: {type}')
        self.priority = type
        print(f'RepoFile -> Priority Now: {self.priority}')