import os
import re
import argparse
from database_handler import SQLiteDatabase
from user_admin_actions import User


def main():
    args = parse_arguments()
    dbname = "users.db"
    connector = SQLiteDatabase(dbname)
    tables = connector.get_table_list()
    connector.drop_all_tables(tables)
    connector.create_tables()

    csv_file_path1 = return_absolute_path(r'data/a/b/users_1.csv')
    csv_file_path2 = return_absolute_path(r'data/a/c/users_2.csv')
    xml_file_path1 = return_absolute_path(r'data/a/b/users_1.xml')
    xml_file_path2 = return_absolute_path(r'data/users_2.xml')
    json_file_path = return_absolute_path(r'data/a/users.json')

    connector.fetch_from_csv(csv_file_path1)
    connector.fetch_from_csv(csv_file_path2)
    connector.fetch_from_xml(xml_file_path1)
    connector.fetch_from_xml(xml_file_path2)
    connector.fetch_from_json(json_file_path)

    connector.remove_duplicates()
    connector.commit()

    user_id, user_role = connector.authorize_user(args.login, args.password)
    user = User(user_id, user_role, connector)
    user.run_action(args.command)

    connector.disconnect()

def parse_arguments():
    def check_login(value):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value) and not re.match(r'^[0-9]{9}$', value):
            raise argparse.ArgumentTypeError(
                "Invalid login. Enter a valid email or a 9-digit phone number."
                )
        return value

    parser = argparse.ArgumentParser(
        description='''User Account Management Script - creates
        a database from contents of "data" folder and runs
        operations on it''')
    parser.add_argument(
        'command',
        choices=[
            'create-database','print-all-accounts', 'print-oldest-account',
            'group-by-age', 'print-children',
            'find-similar-children-by-age'],
        help='Command to be performed on the database'
        )
    parser.add_argument(
        '--login',
        required=True,
        type = check_login,
        help='User login (email or telephone number)'
        )
    parser.add_argument(
        '--password',
        required=True,
        help='User password'
        )
    return parser.parse_args()

def return_absolute_path(relative_path):
    absolute_path = os.path.dirname(__file__)
    result = os.path.join(absolute_path, relative_path)
    return result

if __name__ == "__main__":
    main()
