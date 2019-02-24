# THPWD03 - Work Log

This is the fourth project to team tree house's Python Web Tech Degree. Unlike Work Log from unit 3, this project uses SQLITE with Peewee ORM for the addition and the display of entries.

## Goal
- Build a CLI (command line interface) application that logs what a person has done on a specific day using Peewee ORM and SQLITE. Additionally, refactor work log such that it covers at least 50% of code covered by tests.

## Deliverables / Objectives
1. As a fellow developer, user should find at least 50% of the code covered by tests. User would use coverage.py to validate this amount of coverage.
2. Script must runs without errors. Catch exceptions and report errors to the user in a meaningful way.
3. As a user of the script, a menu should be prompted to choose whether to add a new entry or lookup previous entries.
4. As a user of the script, a task name, a number of minutes spent working on it, and any additional notes must be provided when adding an entry.
5. As a user of the script, search page should presented with four options:
    - find by date
    - find by time spent
    - find by exact search
    - find by pattern
6. When finding by date, user should be able to see a list of dates with entries, and should be presented with options to be able to choose one to see entries from.
7. When finding by time spent, user should be allowed to enter the number of minutes a task took and be able to choose one to see entries from.
8. When finding by an exact string, user should be allowed to enter a string and then be presented with entries containing that string in the task name or notes.
9. When finding by a pattern, user should be allowed to enter a regular expression and then be presented with entries matching that pattern in their task name or notes.
10. When displaying the entries, the entries should be displayed in a readable format with the date, task name, time spent, and notes information.

## Steps to Running the Program
1. For python 2 or python 3 set as default, type command `python main.py`
2. For python 3 users, type command `python3 main.py`

## FAQ
1. Q: How would a user know which version of python is installed as default?
    - A: Type `python --version` in terminal