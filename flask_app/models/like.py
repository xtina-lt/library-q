from flask import session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Like:
    db = "library_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.description = data["description"]
        self.url = data["url"]
        self.count = data["count"]
    
    '''CREATE LIKE'''
    @classmethod
    def validate_insert(cls,data):
        is_true = True
        query="SELECT * FROM users_likes WHERE user_id=%(user_id)s AND like_id=%(like_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            is_true = False
        return is_true

    @classmethod
    def insert(cls, data):
        query="INSERT INTO likes(description, url) VALUES(%(description)s, %(url)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    '''CREATE USER_LIKE'''
    @classmethod
    def insert_like_user(cls, data):
        query="INSERT INTO users_likes(like_id, user_id) VALUES(%(like_id)s, %(user_id)s)"
        result = connectToMySQL(cls.db).query_db(query, data)
        query2 = "UPDATE users SET stars=stars+1 WHERE id=%(user_id)s"
        return connectToMySQL(cls.db).query_db(query2, data)

    '''DELETE'''
    '''like'''
    @classmethod
    def delete(cls, data):
        query="DELETE FROM likes WHERE id=%(like_id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    '''user like'''
    @classmethod
    def delete_user_likes_stars(cls, data):
        query="DELETE FROM users_likes WHERE id=%(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        query2 = "UPDATE users SET stars=stars-1 WHERE id=%(user_id)s"
        return connectToMySQL(cls.db).query_db(query2, data)
    
    @classmethod
    def delete_user_likes(cls, data):
        query="DELETE FROM users_likes WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    '''READ'''
    @classmethod
    def select_all(cls):
        query = "SELECT likes.id AS id, likes.description AS description, likes.url AS url, count(user_id) AS count FROM likes LEFT JOIN users_likes ON users_likes.like_id = likes.id GROUP BY likes.id"
        results = connectToMySQL(cls.db).query_db(query)
        return {i['id'] : cls(i) for i in results}

    @classmethod
    def select_one(cls, data):
        query="SELECT likes.id AS id, likes.description AS description, likes.url AS url, count(user_id) AS count FROM likes LEFT JOIN users_likes ON users_likes.like_id = likes.id WHERE likes.id=%(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def select_by_user(cls,data):
        query="SELECT * FROM users_likes JOIN likes ON likes.id=users_likes.like_id WHERE user_id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        x=[]
        for i in results:
            data={
                'id' : i['id'],
                'description' : i['description'],
                'url' : i['url']
            }
            x.append((data))
        return x