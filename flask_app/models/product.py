from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.like import Like

class Product:
    db="library_schema"
    def __init__(self, data):
        self.id=data["id"]
        self.name=data["name"]
        self.description=data["description"]
        self.url=data["url"]
        self.like=Like.select_one({"id": data["like_id"]})
        self.stars=data["stars"]

    
    @classmethod
    def select_all(cls):
        query="SELECT * FROM products JOIN likes ON likes.id = products.like_id ORDER BY products.created_at DESC"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(i) for i in results]
    
    @classmethod
    def select_user(cls, data):
        query="SELECT * FROM user_obtained_products JOIN products ON products.id = user_obtained_products.product_id WHERE user_id=%(id)s"
        results= connectToMySQL(cls.db).query_db(query, data)
        if results:
            print(results)
            x=[]
            for i in results:
                e={
                    "id": i["products.id"],
                    "name": i["name"],
                    "description": i["description"],
                    "url": i["url"],
                    "like_id": i["like_id"],
                    "stars": i["stars"],
                }
                x.append( cls(e) )
                print(x)
            return x
        else:
            return False
    

    @classmethod
    def insert(cls, data):
        query="INSERT INTO products(name, description, url, like_id, stars) VALUES(%(name)s, %(description)s, %(url)s, %(like_id)s, %(stars)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def check_product_user(cls, data):
        query="SELECT * FROM user_obtained_products WHERE user_id=%(user_id)s AND product_id=%(product_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            flash("You already have that sparkle in your day!")
            return True
        else:
            return False

    @staticmethod
    def validate_product_buy(cost):
        is_valid=True
        user_funds = session["logged_in"]["stars"]
        if cost > user_funds:
            flash(f"You have {user_funds} hearts and the item cost {cost} hearts..")
            flash("Try liking more things!")
            is_valid=False
        return is_valid

    @classmethod
    def user_products_create(cls, data):
        query="INSERT INTO user_obtained_products(user_id, product_id) VALUES(%(user_id)s, %(product_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def product_user_stars(cls, data):
        query="UPDATE users SET stars=stars-%(cost)s WHERE id=%(user_id)s"
        return connectToMySQL(cls.db).query_db(query, data)

