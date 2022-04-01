from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.like import Like
import math
from datetime import datetime

class Reply:
    db = "library_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.user = User.get_stars({"id" : data["user_id"]})
        self.message_id = data["message_id"]
        self.like = Like.select_one({"id": data["like_id"]})
        self.created_at = self.get_time(data["created_at"])
        self.updated_at = self.get_time(data["updated_at"])

    @staticmethod
    def get_time(self):
        now = datetime.now()
        delta = now - self
        # print(f"delta : {delta}, delta.days : {delta.days}, delta.total_seconds() : {delta.total_seconds()}")
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO replies(content, user_id, message_id, like_id) VALUES(%(content)s, %(user_id)s, %(message_id)s, %(like_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query="UPDATE replies SET content=%(content)s WHERE id=%(reply_id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query="DELETE FROM replies WHERE id=%(reply_id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def select_by_message(cls, data):
        query = "SELECT * FROM replies WHERE message_id=%(message_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return [cls(i) for i in results]
        else:
            return False
