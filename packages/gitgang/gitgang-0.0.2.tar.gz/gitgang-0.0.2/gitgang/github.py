# -*- coding: utf-8 -*-

import os.path
import sys
import subprocess
import fnmatch
import yaml
import requests

def members_only(github_org, github_repo, gangfile='gang.yml'):
    """Make sure the latest commit is from a member of the gang.

    Parameters
    ----------
    github_org - string
        The GitHub organization
    github_repo - string
        The GitHub repository
    gangfile - string
        Path to a YAML file with the list of gang members
    """

    # Get the list of members.
    with open(gangfile, 'r') as stream:
        try:
            users = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)

    # Get the files changed in the commits.
    cmd = ['git', 'diff-tree', '--name-only', '-r', 'HEAD']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    # Loop through the lines of output that the above Git command produced.
    for index, line in enumerate(proc.stdout.readlines()):
        change = line.decode('utf-8').strip()
        if index == 0:
            # The first line is the commit ID, which we use to get the Github user.
            github_api_request = "https://api.github.com/repos/%s/%s/commits/%s" \
                % (github_org, github_repo, change)
            try:
                response = requests.get(github_api_request).json()
            except requests.exceptions.RequestException as e:
                print(e)
                sys.exit(1)

            # Exit now if the author is an administrator.
            user = response['author']['login']
            if user in users and 'administrator' == users[user]:
                sys.exit(0)

            # Exit now if the user is not listed.
            if user not in users:
                raise RuntimeError("User '%s' is not listed in %s." % (user, gangfile))

        else:
            # The rest of the lines of output are files that were changed.
            change_allowed = False
            for allowed_path in users[user]:
                if fnmatch.fnmatch(change, allowed_path):
                    change_allowed = True

            if not change_allowed:
                raise RuntimeError("Changed file '%s' not an allowed path for user '%s'." % (change, user))
