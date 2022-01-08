from pathlib import Path


def show_cmd(task):
    return "executing... %s" % task.name

def task_clean_main():
    action_path = Path("src/data-cleaning/clean-main.py")
    return {
        "file_dep": [Path("data/main/cornelia-raw.csv")],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/cleaned/cornelia-cleaned.csv")],
        "title": show_cmd
    }