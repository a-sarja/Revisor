import os

rules_dirs = ["crowd_sourced_yara_rules", "custom_yara_rules"]


for rules_dir in rules_dirs:
    if not os.path.exists(rules_dir):
        os.makedirs(rules_dir)

#download crowdsourced yara repositories

with open("yara_git_repos.txt", "r") as yara_git_repo: 
    repos = yara_git_repo.readlines()
    os.chdir(rules_dirs[0])

    for repo in repos:
        os.system(f'git clone {repo}')