from app.model.PriorityType import PriorityType
from app.model.RepoFile import RepoFile

def is_not_already_added(file, list):
    for item in list:
        if file.filename == item.filename:
            return False
    return True