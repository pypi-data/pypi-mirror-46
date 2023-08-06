# gitgang
Reject pull-requests that are not from members of your gang.

## Overview

This is meant to be used in combination with a CI tool/service. It is a poor-man's access-control for limiting who can submit pull-requests to a public GitHub repository.

GitHub usernames are used to check access. Access control can be granular by specifying files/folders (with wildcards), or a user can be an 'administrator' and have access to all files.

## Usage

1. Create a YAML file with a list of GitHub usernames. For each username:
    * Either assign 'administrator'
    * Or assign a list of allowed paths

    Example:
    ```
    docdude632:
        - docs/*
    bigboss43: administrator
    montypython3:
        - lib/*
        - composer.json
    HR_managr:
        - gang.yml
    ```
2. Run a script that calls the members_only() function. Example:
    ```
    from gitgang.github import members_only

    members_only(github_org='brockfanning', github_repo='gitgang', gangfile='gang.yml')
    ```

An exception means that the PR should be rejected. If nothing happens, the PR is good to go.

Use your preference of CI tools/services, and make sure the script is run for each pull-request that is opened.
