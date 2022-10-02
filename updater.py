#!/usr/bin/env python
import os
import subprocess
import sys
import logging


def run_command(command):
    if not isinstance(command, list):
        raise TypeError
    process = subprocess.run(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    if process.stderr.decode('utf-8') == '':
        print(process.stdout.decode('utf-8'))
        return
    raise Exception


def check_git_repo_exists():
    process = subprocess.run(['git', 'status'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    if process.stdout.decode('utf-8') == '':
        return False
    return True


def get_dir_exists(path):
    return os.path.exists(path)


def check_for_repo_and_pull(path):
    if get_dir_exists(path) == True:
        os.chdir(path)
        if check_git_repo_exists() == True:
            try:
                run_command(['git', 'pull'])
            except:
                logging.error('Git pull failed for path ' + str(path))

def add_all_and_push():
    pass

def check_current_branch():
    pass

def main():
    with open('sources.txt', 'r') as f:
        data = f.readlines()
        check_for_repo_and_pull(data[0])


if __name__ == "__main__":
    main()
