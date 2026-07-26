# Git & GitHub Cheatsheet

Git is a version control system that tracks changes in your code. Here are the basic commands to get you started.

## Configuration (First Time Setup)
- `git config --global user.name "Your Name"`
- `git config --global user.email "your.email@example.com"`

## Starting a Repository
- `git init`: Initialize a new local Git repository
- `git clone [url]`: Clone a remote repository to your local machine

## Tracking Changes
- `git status`: Check the status of your working directory (shows modified, staged, and untracked files)
- `git add [file]`: Add a file to the staging area
  - `git add .`: Add all changed files to the staging area
- `git commit -m "Commit message"`: Commit staged changes with a descriptive message

## Branching
- `git branch`: List all local branches
- `git branch [branch_name]`: Create a new branch
- `git checkout [branch_name]`: Switch to a specific branch
  - `git checkout -b [branch_name]`: Create and switch to a new branch in one command
- `git merge [branch_name]`: Merge the specified branch into the current branch

## Syncing with Remote
- `git remote -v`: List remote repositories
- `git fetch`: Fetch updates from the remote repository (does not merge)
- `git pull`: Fetch and merge changes from the remote repository
- `git push origin [branch_name]`: Push your local branch commits to the remote repository

## Helpful Tools
- `git log`: View the commit history
- `git diff`: Show differences between working directory and the staging area
