import random

from flask import flash

from app.model.PriorityType import PriorityType
from app.model.RepoFile import RepoFile

LOW_PRIORITY_COLOR = '#198754'
MEDIUM_PRIORITY_COLOR = '#ffc107'
HIGH_PRIORITY_COLOR = '#dc3545'
NORMAL_PRIORITY_COLOR = '#0d6efd'

PRIORITY_COLORS = [
    LOW_PRIORITY_COLOR,
    MEDIUM_PRIORITY_COLOR,
    HIGH_PRIORITY_COLOR,
    NORMAL_PRIORITY_COLOR
]


def is_not_already_added(file, list):
    for item in list:
        if file.filename == item.filename:
            return False
    return True


def find_max_metric_value(metric: str, repo_file_list: list):
    try:
        max_metric = repo_file_list[0].get_metric(metric)
        for file in repo_file_list:
            curr_metric = file.get_metric(metric)
            if curr_metric > max_metric:
                max_metric = curr_metric
        return max_metric
    except IndexError:
        flash('No commits in the repository')

def find_hotspot_priority(max_cc, max_churn, file_cc, file_churn):
    print(f"MAX CHURN: {max_churn} | MAX CC: {max_cc}")
    print(f"CHURN: {file_churn} | CC: {file_cc}")
    threshold_churn = max_churn / 2
    threshold_cc = max_cc / 2
    if file_cc <= threshold_cc:
        if file_churn <= threshold_churn:
            return 'LOW'
        if file_churn >= threshold_churn:
            return 'NORMAL'
    if file_cc >= threshold_cc:
        if file_churn <= threshold_churn:
            return 'MEDIUM'
        if file_churn >= threshold_churn:
            return 'HIGH'
    else:
        return None