###############
''' IMPORTS '''
###############
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app) 
import re
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")


###############
'''  CLASS  '''
###############
class User:
    db = 'library_schema'
    # global variable
    # SQL: schema.table == users_schema.users

    def __init__(self, data):
    # {'first_name': 'xxxxx', 'last_name': 'xxxx', 'email':'xxxx@xxxx.com', 'password':'xxxxxxxx'}
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.stars = data["stars"]


    ############
    ''' READ '''
    ############
    '''READ ALL'''
    @classmethod
    def select_all(cls):
        query="SELECT * FROM users"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(i) for i in results]

    '''READ ONE'''
    @classmethod
    def select_one(cls, data):
        query="SELECT * FROM users WHERE id=%(id)s"
        result=connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def is_email(cls,data):
        query="SELECT * FROM users WHERE email=%(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return results[0]
        else:
            return False

    @classmethod
    def get_password(cls, data):
        query="SELECT password FROM users WHERE email=%(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]

    ##################
    ''' FUNCTIONAL '''
    ##################
    @classmethod
    def get_stars(cls, data):
        query="SELECT * FROM users WHERE id=%(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        r = result[0]
        return {"id": r["id"], "first_name": r["first_name"], "stars":r["stars"]}
    
    @classmethod
    def get_stars_email(cls, data):
        query="SELECT * FROM users WHERE email=%(email)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        r = result[0]
        return {"id": r["id"], "first_name": r["first_name"], "stars":r["stars"]}

    ############
    '''LOGIN'''
    ############
    @staticmethod
    def validate_login(e):
        is_valid = True
        email=User.is_email(e)
        if email:
            if not bcrypt.check_password_hash(email['password'], e["password"]):
                flash("Incorrect password", "login")
                is_valid=False
        else:
            flash("Not a valid email", "login")
            is_valid=False
        return is_valid

    #######################
    '''CREATE / REGISTER'''
    #######################
    '''VALIDATE'''
    @staticmethod
    def validate_insert(e):
        is_valid=True
        '''name lengths'''
        if len(e["first_name"]) < 3:
            flash("First name should be greater than 3 characters","register")
            is_valid=False
        if len(e["last_name"]) < 3:
            flash("Last name should be greater than 3 characters", "register")
            is_valid=False
        '''email'''
        if not EMAIL_REGEX.match(e["email"]):
            flash("Not a valid email", "register")
            is_valid=False
        if e["email"] != e["check_email"]:
        # 2) check if emails match
            flash("Emails are not the same🤷‍♀️", "register")
            is_valid=False
        if User.is_email(e):
            flash("Email in use 😞","register")
            is_valid=False
        '''password'''
        if e["password"] != e["check_pword"]:
            flash("Passwords do not match", "register")
            is_valid=False
        if not PASSWORD_REGEX.match(e["password"]):
            flash("Password must contain: 1 upper, 1 lower, 1 special character, 1 number.", "register")
            is_valid=False
        return is_valid

    '''QUERY'''
    @classmethod
    def insert(cls, data):
        query="INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)
        # returns id
    
    ############
    '''UPDATE'''
    ############
    '''VALIDATE'''
    @staticmethod
    def validate_update(e):
        is_valid=True
        found_email = User.is_email(e)
        found_user = User.select_one(e)

        '''name lengths'''
        if len(e["first_name"]) < 3:
            flash("First name should be greater than 3 characters")
            is_valid=False
        if len(e["last_name"]) < 3:
            flash("Last name should be greater than 3 characters")
            is_valid=False
        '''email'''
        if found_email and found_email["email"] != found_user.email:
            flash("Email taken, and not by you🤷‍♀️")
            is_valid=False
        if not EMAIL_REGEX.match(e["email"]):
            flash("Invalid email")
            is_valid=False
        if e["email"] != e["confirm_email"]:
            flash("Emails are not the same🤷‍♀️")
            is_valid=False
        '''password'''
        if not bcrypt.check_password_hash(found_user.password, e["password"]):
            flash("Present password doesn't match")
            is_valid=False
        if e["new_pass"]:
            if e["new_pass"] != e["new_pass_check"]:
                flash("Passwords do not match🤷‍♀️")
                is_valid=False
            if not PASSWORD_REGEX.match(e["new_pass"]):
                flash("Password must contain: 1 upper, 1 lower, 1 special character, 1 number.")
                is_valid=False
        return is_valid

    '''QUERY'''
    @classmethod
    def update(cls, data):
        query="UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query,data)

    ############
    '''DELETE'''
    ############
    @classmethod
    def delete(cls, data):
        query="DELETE FROM users WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query,data)