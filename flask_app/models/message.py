from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.reply import Reply
import math
from datetime import datetime

class Message:
    db = "library_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.sender = User.get_stars({"id" : data["sender_id"]})
        self.reciever = User.get_stars({"id" : data["reciever_id"]})
        self.created_at = Message.get_time(data["created_at"])
        self.updated_at = Message.get_time(data["updated_at"])
        self.like_id = data["like_id"]
        self.has_replies = Reply.select_by_message({"message_id": data["id"]})
    
    @staticmethod
    def get_time(e):
        now = datetime.now()
        delta = now - e
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"
    
    @classmethod
    def create(cls, data):
        query="INSERT INTO messages(content, sender_id, reciever_id, like_id) VALUES(%(content)s, %(sender_id)s, %(reciever_id)s, %(like_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def read_recieved(cls, data):
        query="SELECT * FROM messages WHERE reciever_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return [cls(i) for i in results]
        else:
            return False
    
    @classmethod
    def read_sent(cls, data):
        query="SELECT * FROM messages WHERE sender_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return [cls(i) for i in results]
        else:
            return False
    
    @classmethod
    def update(cls, data):
        query="UPDATE messages SET content=%(content)s WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query="DELETE FROM messages WHERE id=%(message_id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def select_one(cls, data):
        query="SELECT * FROM replies JOIN messages ON messages.id = replies.message_id WHERE messages.id=%(mesage_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            e = results[0]
            message_data = {
                "id": e["messages.id"],
                "content": e['messages.content'],
                "sender_id": e["sender_id"],
                "reciever_id": e["reciever_id"],
                "like_id": e['like_id'],
                "created_at": e["messages.created_at"],
                "updated_at": e["messages.updated_at"]
            }
            message = cls(message_data)
            for i in results:
                message.has_replies.append( Reply(e) )
            return message
        else:
            q="SELECT * FROM messages WHERE id=%(message_id)s"
            r=connectToMySQL(cls.db).query_db(q, data)
            return cls(r[0])
