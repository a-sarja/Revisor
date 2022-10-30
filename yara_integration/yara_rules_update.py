import os
from zoneinfo import available_timezones

rules_dir = "crowd_sourced_yara_rules"

available_dirs = os.listdir(rules_dir)

for dir in available_dirs:
    cur_wd = os.getcwd()
    new_wd = os.getcwd() + '/' + rules_dir + '/' + dir
    os.chdir(new_wd)
    print(os.system('git pull'))
    os.chdir(cur_wd)