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