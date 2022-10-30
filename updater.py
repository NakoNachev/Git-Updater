#!/usr/bin/env python
import os
import subprocess
import logging
import time
import sys

def run_command(command):
    if not isinstance(command, list):
        raise TypeError
    process = subprocess.run(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    if process.stderr.decode('utf-8') == '':
        return process
    raise Exception


def check_git_repo_exists() -> bool:
    process = subprocess.run(['git', 'status'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    if process.stdout.decode('utf-8') == '':
        return False
    return True


def get_dir_exists(path) -> bool:
    return os.path.exists(path)


def check_for_repo_and_pull(path) -> None:
    logger.info('Pulling from origin')
    if get_dir_exists(path) == True:
        os.chdir(path)
        if check_git_repo_exists() == True:
            try:
                run_command(['git', 'pull'])
            except:
                logger.error('Git pull failed for path ' + str(path))


def add_all_and_push() -> None:
    try:
        run_command(['git', 'add', '.'])
        run_command(
            ['git', 'commit', '-m', generate_commit_message()])
        run_command(['git', 'push'])
    except:
        logger.error('Adding all files failed')


def generate_commit_message() -> str:
    return '\"Automated commit from python updater ' + str(time.time()) + '\"'


def get_current_branch() -> str:
    """ Executes git status and returns the decoded branch from the stdout"""
    try:
        data = run_command(['git', 'branch', '--show-current'])
        return data.stdout.decode('utf-8')
    except:
        logger.error('Check status failed')


def branch_has_changes() -> bool:
    if run_command(['git', 'status']).stdout.decode('utf-8').find('nothing to commit') == -1:
        return True
    return False


def main():
    global logger
    logger = set_up_logger()
    sources_file = 'sources.txt'
    logger.info('Starting updater')
    try:
        with open(sources_file, 'r') as f:
            data: list[str] = f.readlines()
            for line in data:
                logger.info('Reading target source ' + str(line) )
                check_for_repo_and_pull(data[0])
                if branch_has_changes() == True:
                    print("has changes")
                    add_all_and_push()
                else:
                    logger.info('No changes found, skipping pushing to origin')
    except FileNotFoundError:
        logger.error('Target file {} not found'.format(sources_file))
        return sys.exit(1)

def check_for_uncommited_commits():
    pass

def set_up_logger():
    logging.basicConfig(filename='output.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    return logging.getLogger('updater')

if __name__ == "__main__":
    target_dir = r"C:\Users\nakon\Desktop\Docs\dev\git_updater"   # r in front of the string is for signalling raw string, a.k.a wont escape characters
    try: 
        os.chdir(target_dir)
    except:
        logging.error('Could not cd to target directory {}'.format(target_dir))
        sys.exit(1)
    main()