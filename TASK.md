## Recruitment Task Directions

### IMPORTANT UPDATE 
Data files has been updated to alleviate uncertainty about telephone number processing

### Background
We have a dataset containing information about individuals, including their first name, telephone number, email, password, role, date of account creation and a list of children with their names and ages. We would like you to build a script/CLI that performs some operations on the data.

### Specifications
1. The dataset is distributed across multiple files(JSON, XML and CSV).

2. The information is structured as follows:
   - `firstname`
   - `telephone_number`
   - `email`
   - `password in plaintext`
   - `role(admin/user)`
   - `created_at` date in format YYYY-MM-DD HH:MM:SS
   - List of children with `(name, age)`
   
 In the csv file, individual children data is delimitated by a comma, columns are delimited by a semicolon.
	
### Important!
- **Importing Data**
    - Validate emails - validation criteria is listed below, reject entries without a valid email address
    - Reject entries without provided telephone number
    - Remove duplicates(by telephone number or email) from the merged dataset. Save the newer entry based on the timestamp.
    - Store telephone numbers as 9 digits, remove any special characters and leading zeros (+48123456789, 00123456789, (48) 123456789, 123 456 789, all of these should be stored as 123456789)
    - All telephone numbers has been generated in a way that after removing special chars and leading zeros, there will always be a valid 9-digit number. For the purposes of this exercise you can omit further validation.	

- **Validation Criteria for Emails:**
  - Email must contain only one "@" symbol.
  - The part before "@" must be at least 1 character long.
  - The part between "@" and "." must be at least 1 character long.
  - The part after the last "." must be between 1 and 4 characters long, containing only letters and/or digits.
    regex = '^[a-zA-Z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{1,4}$'

- **Example inputs and outputs do not relate to the provided data!**
### Tasks
- Each task requires a login. Login is executed by passing ` --login <login> --password <password> ` such that script commands will look like `python script.py <command> --login <login> --password <password>` in order to work.
- Login is either the users email or their 9-digit telephone number, implement both options to the code.
- Some functionality is reserved for admin users, but admin users can execute base user commands.
- Each task has a specified command and an expected output, make sure these are according to the specification below.
- Missing login, password or incorrect credentials should result in following output `Invalid Login` 

### Admin Actions
- **Print The Number of All Valid Accounts** DONE
  - Command: `python script.py print-all-accounts`
  - Print the total number of valid accounts.
  - Expected output: integer
  
         >python script.py print-all-accounts --login 555123456 --password sASfC1234
         1233333
         
- **Print The Longest Existing Account** DONE
    - Command: `python script.py print-oldest-account`
    - Print information about the account with the longest existence.
    - Expected output: 

            >python script.py print-oldest-account --login 555123456 --password sASfC1234
            name: Boris
	        email_address: boris@gmail.com
	        created_at: 1990-12-12 13:20:00


- **Group Children by Age** DONE
  - Command: `python script.py group-by-age`
  - Group children by age and display relevant information.
  - Expected output: list of rows according to the example, sorted by count - ascending.
  
         >python script.py group-by-age --login 555123456 --password sASfC1234
         age: 12, count: 5
         age: 10, count: 7
         
### User Actions
- **Print Children** DONE
  - Command: `python script.py print-children`
  - Display information about the user's children. Sort children alphabetically by name.
  - Expected output: list of rows containing `<name>, <age>`

         >python script.py print-children --login 555123456 --password sASfC1234
         Adam, 2
         Sally, 12


- **Find Users with Children of Same Age**
  - Command: `python script.py find-similar-children-by-age`
  - Find users with children of the same age as at least one own child, print the user and all of his children data. Sort children alphabetically by name.
  - Expected output: list of rows containing `<name-of-parent>,<parents-telephone-number>: <matched-child-name>, <matched-child-age>; <matched-child-name>, <matched-child-age>`
  
         >python script.py find-similar-children-by-age --login 555123456 --password sASfC1234
         Brock, 789543123: Bart, 4; Olive, 2
         John, 432764512: Sally, 2
   
## Extra points for:
- tests
- error handling
- adding a command `python script.py create_database` to create an SQLite database and then using it for the rest of the tasks

## Rules & hints
- use Python 3.10+
- Remeber to use the commands provided in the task names
- Follow the format of the answers as in provided examples
- **use OOP paradigm**
- You are free to use any third-party libraries
- Provide README with examples of how to use your script
- Write Python code that conforms to PEP 8
- Remember about validating input data,
- Please handle possible exceptions within the script in a user-friendly way
- Please put your solution in a private repository on Github and invite reviewer@profil-software.com as a collaborator (any role with at least read-only access to code) -> https://docs.github.com/en/github/setting-up-and-managing-your-github-user-account/inviting-collaborators-to-a-personal-repository
