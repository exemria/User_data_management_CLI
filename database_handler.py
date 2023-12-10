import csv
import json
import sqlite3
import xml.etree.ElementTree as ET
import re
import sys


class SQLiteDatabase:

    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def disconnect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def execute(self):
        self.cur.execute()
    
    def get_table_list(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return self.cur.fetchall()

    def drop_all_tables(self, tables):
        for table in tables:
            self.cur.execute(f"DROP TABLE IF EXISTS {table[0]}")
        self.conn.commit()

    def create_tables(self):
        try:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id integer primary key,
                firstname text,
                telephone_number numeric ,
                email text,
                password varchar(100),
                role text,
                created_at numeric,
                children varchar(100) 
                )
                """)
            return self.cur.fetchall()
        except Exception as e:
            print("Error table not created:",e)

    def authorize_user(self, login, password):
        try:
            auth_option = 'email' if '@' in login else 'telephone_number' 
            self.cur.execute(f'SELECT ID, ROLE FROM users WHERE {auth_option}="{login}" AND password="{password}"')
            match = self.cur.fetchone()
            if match:
                print(f"Found matching user with id: {match[0]} and role: {match[1]}")
                return match[0], match[1]
            else:
                raise PermissionError()
            
        except PermissionError as e:
            print("Access denied - invalid credentials!", e)
            sys.exit(1)

    def validate_telephone_number(self, number):
        pattern = r'^(?:00)?(?:\+?48)?(?:\s?|-)?(\d{3})(?:\s?|-)?(\d{3})(?:\s?|-)?(\d{3})$'
        match = re.search(pattern, number)

        if match:
            phone_number = ''.join(match.groups())
            phone_number = phone_number[-9:]
            return phone_number
 
    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{1,4}$'
        if re.match(email_regex, email):
           return email

    def remove_duplicates(self):
        try:
            self.cur.execute('''
                DELETE FROM users
                WHERE rowid NOT IN (
                    SELECT MIN(rowid)
                    FROM users
                    GROUP BY telephone_number, email 
                    )
            ''')
            self.conn.commit()
            print("Duplicates removed successfully")
            
        except Exception as e:
            print('Error removing duplicates:', e)

    def fetch_from_xml(self, file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            for user in root.findall('user'):
                firstname = user.find('firstname').text
                telephone_number = user.find('telephone_number').text
                email = user.find('email').text
                password = user.find('password').text
                role = user.find('role').text
                created_at = user.find('created_at').text
                
                children = user.find('children')
                if children:
                    children_data = ','.join([
                        f"{child.find('name').text} ({child.find('age').text})" 
                        for child in children.findall('child')
                    ])
                else:
                    children_data = ''.join("null")
                telephone_number = self.validate_telephone_number(telephone_number)
                email = self.validate_email(email)
                
                if email and telephone_number is not None:
                    self.cur.execute("""
                        INSERT INTO users (firstname, telephone_number, email, password, role, created_at, children)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (firstname, telephone_number, email, password, role, created_at, children_data))
                    self.conn.commit()
                    print("XML user added")
                else:
                    print(f"XML file entry not added: {firstname}, {email}, {telephone_number}, {password}")

        except Exception as e:
            print("Error inserting XML data:", e)

    def fetch_from_csv(self, file_path):
        try:
            with open(file_path, 'r', encoding = 'utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter= ';')
                next(reader)
                for row in reader:
                    row = ['null' if cell == '' else cell for cell in row]

                    telephone_number = row[1]
                    email = row[2]
                  
                    telephone_number = self.validate_telephone_number(telephone_number)
                    email = self.validate_email(email)
                    if email and telephone_number is not None:
                        self.cur.execute("""
                            INSERT INTO users (firstname, telephone_number, email, password, role, created_at, children)
                            VALUES( ?, ?, ?, ?, ?, ?, ?)
                        """, row)
                        print("csv user added.")
                        self.conn.commit()

                    else:
                        print('csv file not added.')
                                         
        except Exception as e:
            print('Error inserting csv data to users table', e)

    def fetch_from_json(self, file_path):
        try:
            with open(file_path) as f:
                users = json.load(f)
            for user_data in users:
                firstname = user_data.get('firstname')
                telephone_number = user_data.get('telephone_number')
                email = user_data.get('email')
                password = user_data.get('password')
                role = user_data.get('role')
                created_at = user_data.get('created_at')
                children = user_data.get('children', [])

                if children:

                    children_str = ','.join([f"{child.get('name')} ({child.get('age')})" for child in children])
                else:
                    children_str = ''.join("null")
                
                telephone_number = self.validate_telephone_number(telephone_number)
                email = self.validate_email(email)
                
                if email and telephone_number is not None:
                        self.cur.execute("""
                            INSERT INTO users (firstname, telephone_number, email, password, role, created_at, children)
                            VALUES( ?, ?, ?, ?, ?, ?, ?)
                        """, (firstname, telephone_number, email, password, role, created_at, children_str))
                        self.conn.commit()
                        print("Json user added")
                else:
                    print(f"Rejected json data for user: {firstname}, {email}")

        except Exception as e:
            print("Error inserting json user data:", e)
