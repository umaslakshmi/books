""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create_user(self, info):
        #validations
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if len(info['name']) < 2:
            errors.append("Name must be at least 2 characters")
        if not EMAIL_REGEX.match(info['email']):
            errors.append("Invalid email format")
        if len(info['password']) < 8:
            errors.append("Password must be at least 8 characters")
        elif info['password'] != info['confirm_password']:
            errors.append("Passwords do not match")

        if errors:
            return {'status': False, 'errors': errors}

        query = 'INSERT INTO users (name, alias, email, pw_hash, created_at, updated_at) VALUES (:name, :alias, :email, :pw_hash, NOW(), NOW())'
        data = {
            'name': info['name'],
            'alias': info['alias'],
            'email': info['email'],
            'pw_hash': self.bcrypt.generate_password_hash(info['password'])
        }
        self.db.query_db(query, data)

        get_user_query = 'SELECT * FROM users ORDER BY id DESC LIMIT 1'
        users = self.db.query_db(get_user_query)
        return {'status': True, 'user': users[0]}

    def check_user(self, info):
        query = 'SELECT * FROM users WHERE email=:email'
        data = {'email': info['email']}
        users = self.db.query_db(query, data)
        if users:
            user = users[0]
            if self.bcrypt.check_password_hash(user['pw_hash'], info['password']):
                return user
        return False

    def get_user_by_id(self, id):
        query = 'SELECT * FROM users WHERE id=:id'
        data = {'id': id}
        users = self.db.query_db(query, data)
        return users[0]



    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """