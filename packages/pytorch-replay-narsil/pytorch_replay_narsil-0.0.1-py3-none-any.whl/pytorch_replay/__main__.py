import argparse
import datetime
import git
import subprocess
from . import PREFIX


def replay(repo, experiment_id):
    print(f"Replaying: {experiment_id}")
    experiments = get_experiments(repo)
    ok_experiments = [
        experiment for experiment in experiments if experiment["id"] == experiment_id
    ]
    if len(ok_experiments) == 0:
        raise Exception(f"Cannot find experiment {experiment_id}.")
    elif len(ok_experiments) > 1:
        raise Exception(f"Duplicate ids for experiment {experiment_id}")

    experiment = ok_experiments[0]

    previous = repo.active_branch
    if previous is None:
        previous = repo.head.object.hexsha

    print(f'Replaying: {experiment["command"]} on commit {experiment["commit"]}')
    try:
        repo.git.checkout(experiment["commit"])
        subprocess.call(experiment["command"], shell=True)
        repo.git.checkout(previous)
    except (KeyboardInterrupt, Exception):
        repo.git.checkout(previous)


def scan_line(line):
    tokens = line.split('"')
    command = tokens[1].strip()
    date = datetime.datetime.strptime(tokens[2].strip(), "%Y-%m-%d %H:%M:%S.%f")
    id = tokens[0].split(":")[1].strip()
    return {"date": date, "command": command, "id": id}


def get_experiments_from_commit(commit):
    experiments = []
    for line in commit.message.split("\n"):
        if line.startswith(PREFIX):
            try:
                experiment = scan_line(line)
            except Exception:
                continue
            experiment["commit"] = commit.hexsha
            experiments.append(experiment)
    return experiments


def get_experiments(repo):
    commits = repo.iter_commits("--all", max_count=100, since="10.days.ago")
    experiments = []
    for commit in commits:
        commit_experiments = get_experiments_from_commit(commit)
        experiments.extend(commit_experiments)

    return experiments


def list_experiments(repo):
    experiments = get_experiments(repo)
    if len(experiments) == 0:
        print("No experiments where found, be sure to use setup() correctly")
        return
    print("Experiments :")
    print(f'Date{" "*22} {"Id":6} {"Commit":40} {"Command":20}')
    for experiment in experiments:
        print(
            f'{experiment["date"]} {experiment["id"]:6} {experiment["commit"]:40} {experiment["command"]:20}'
        )


def main():
    parser = argparse.ArgumentParser(description="Replay a saved experience.")
    parser.add_argument(
        "experiment", metavar="EXPERIMENT", help="The id of the experiment", nargs="?"
    )
    args = parser.parse_args()
    repo = git.Repo(search_parent_directories=True)
    if args.experiment is None:
        list_experiments(repo)
    else:
        replay(repo, args.experiment)


if __name__ == "__main__":
    main()
