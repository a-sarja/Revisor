import os

rules_dir = "crowd_sourced_yara_rules"

if not os.path.exists(rules_dir):
    os.makedirs(rules_dir)


with open("yara_git_repos.txt", "r") as yara_git_repo: 
    repos = yara_git_repo.readlines()
    os.chdir(rules_dir)

    for repo in repos:
        os.system(f'git clone {repo}')