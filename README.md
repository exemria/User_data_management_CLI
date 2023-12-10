# profil_software
recruitment project from Profil Software

- Martyna Buczek
- email: mbuczek.dev@gmail.com
- phone_number: +48 784 408 800


### USER DATA MANAGEMENT CLI ###

### About the code

This program manages a dataset containing user information in various formats (JSON, XML, CSV). The program offers functionalities to import, validate, and perform operations on user data.

### Technologies used

- Python 3.10+: Core programming language. Used standard libraries such as csv, json, sqlite3, xml.etree.ElementTree, datetime, re, and sys.
- SQLite: Database management system for data storage and retrieval.
- Third-party Libraries:
    - tabulate: Used for generating tables from data
    - termcolor: Enables colored text output in the terminal
    - unittest: Module for writing and running tests.
       
### Requirements

- python 3.10 or higher
- SQLite
- dependencies

To install the necessary dependencies, run:
`pip install -r requirements.txt`

### Usage

The CLI supports multiple actions, accessible via commands:

## Login

The login can be performed using either the user's email or their 9-digit telephone number.
`python script.py <command> --login <login> --password <password>`

## Actions available for admin

- Print The Number of All Valid Accounts
`python script.py print-all-accounts --login <login> --password <password>`
This command prints the total number of valid accounts.

- Print The Longest Existing Account
`python script.py print-oldest-account --login <login> --password <password>`
Displays information about the account with the longest existence.

- Group Children by Age
`python script.py group-by-age --login <login> --password <password>`
Groups children by age and displays relevant information.

## Actions available for user 

- Print Children
`python script.py print-children --login <login> --password <password>`
Displays information about the user's children sorted alphabetically by name.

- Find Users with Children of Same Age
```python script.py find-similar-children-by-age --login <login> --password <password>```
Finds users with children of the same age as at least one of their own children. Displays user and children data sorted alphabetically by name.

### Structure

- script.py: Main script handling user actions and interactions
- database_handler.py: Manages SQLite database operations
- user_admin_actions.py: Contains classes for admin and user actions
- users.db: SQLite database file