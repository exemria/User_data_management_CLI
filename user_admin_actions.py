import re
import sys
from datetime import datetime


class User:
    def __init__(self, id, role, conn):
        self.role = role
        self.id = id
        self.conn = conn

    def run_action(self, action):
        action = action.replace('-', '_')
        try:
            if hasattr(UserActions, action):
                getattr(UserActions(self.id, self.conn), action)()
                return
            if hasattr(AdminActions, action):
                if self.role == 'admin':
                    getattr(AdminActions(self.id, self.conn), action)()
                    return
                else:
                    raise PermissionError()
            else:
                raise AttributeError()
        except PermissionError:
            print(
                "Permission error - this user is not authenticated to do this action"
            )
            sys.exit(1)


class AdminActions:
    def __init__(self, id, conn):
        self.id = id
        self.conn = conn

    def print_all_accounts(self):
        self.conn.cur.execute(" SELECT COUNT(*) FROM users ")
        accounts = self.conn.cur.fetchall()[0]
        for number in accounts:
            print(number)

    def print_oldest_account(self):
        self.conn.cur.execute("select firstname, email, created_at from users order by created_at asc limit 1")
        row = self.conn.cur.fetchone()
        if row:
            formatted_data = {
                'name': row[0],
                'email_address': row[1],
                'created_at': datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            }

            for key, value in formatted_data.items():
                print(f"{key}: {value}")

    def group_by_age(self):
        self.conn.cur.execute(" SELECT children FROM users")
        children_data = self.conn.cur.fetchall()
        age_count = {}

        for row in children_data:
            children_str = row[0]
            if children_str != 'null':
                children_str_list = children_str.split(',')

                for child_data in children_str_list:
                    child_age = int(child_data.split("(")[1].rstrip(")"))
                    if child_age in age_count:
                        age_count[child_age] += 1
                    else:
                        age_count[child_age] = 1

        dict_order_by_age = sorted(age_count.items(), key = lambda item: item[0])
        dict_order_by_value = sorted(dict_order_by_age, key = lambda item: item[1])
        formatted_data = [f"age: {age}, count: {count}" for age, count in dict_order_by_value]
        print("\n".join(formatted_data))


class UserActions:
    def __init__(self, id, connector):
        self.id = id
        self.connector = connector
    
    def _get_own_children(self):
        self.connector.cur.execute(f"SELECT children FROM users WHERE id = {self.id}")
        own_children_data = self.connector.cur.fetchall()
        for row in own_children_data:
            children_str = row[0]
            if children_str != 'null':
                children_list = children_str.split(',')
        return children_list

    def print_children(self):
        children_list = self._get_own_children()
        for child in children_list:
            split_name_age = child.split("(")
            name = split_name_age[0].strip()
            age = split_name_age[1].rstrip(')')
            print(f"{name}, {age}")

    def find_similar_children_by_age(self):
        children_list = self._get_own_children()
        user_children_age = set()
        for child in children_list:
            split_name_age = child.split("(")
            user_children_age.add(split_name_age[1].rstrip(')'))
        users = self.users_dict()

        matched_children = {}
        for user in users:
            if user['id'] != self.id:
                for child_name, child_age in user['children'].items():
                    if child_age in user_children_age:
                        if user['firstname'] not in matched_children:
                            matched_children[user['firstname']] = {'telephone_number': user['telephone_number'], 'children': {}}
                        matched_children[user['firstname']]['children'][child_name] = child_age
        
        for parent_name, data in matched_children.items():
            telephone_number = data['telephone_number']
            children_info = data['children']
            sorted_children_info = sorted(children_info.items(), key=lambda x: x[0])
            children_data = '; '.join([f"{child}, {age}" for child, age in sorted_children_info])
            print(f"{parent_name}, {telephone_number}: {children_data}")

    def users_dict(self):
        self.connector.cur.execute("""
                            SELECT * FROM users
                        """)
        users_row = self.connector.cur.fetchall()
        column_names = ['id','firstname', 'telephone_number', 'email', 'password', 'role', 'created_at', 'children']

        result_list = []
        for row in users_row:
            row_dict = {}
            children_dict = {}
            children_data = row[7]
            if children_data != 'null':
                children_list = children_data.split(',')
                for child_info in children_list:
                    split_name_age = child_info.split("(")
                    child_name = split_name_age[0].strip()
                    child_age = split_name_age[1].rstrip(')')
                    children_dict[child_name] = child_age

            for i in range(len(column_names)):
                if column_names[i] == 'children':
                    row_dict['children'] = children_dict
                else:
                    row_dict[column_names[i]] = row[i]
            result_list.append(row_dict)
        return result_list
