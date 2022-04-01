from flask_app.config.mysqlconnection import connectToMySQL
from flask import session

class Project:
    db="library_schema"
    def __init__(self, data):
        self.id=data["id"]
        self.name=data["name"]
        self.description=data["description"]
        self.like= data['like']
        self.git=data["git"]
        self.path=data["path"]
        self.url=data["url"]
        self.categories = self.get_categories(data)

    @classmethod
    def get_categories(cls, data):
        query = "SELECT * FROM projects_categories JOIN categories ON categories.id = projects_categories.category_id WHERE project_id = %(id)s and categories.name != 'None' and categories.name != ' ' "
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            x = ", ".join([i['name'] for i in results])
            return x
        else:
            return 'NULL'
    
    @classmethod
    def select_all_json(cls):
        query="SELECT *, count(users_likes.user_id) AS likes_count FROM projects JOIN likes ON likes.id = projects.like_id LEFT JOIN users_likes ON users_likes.like_id = likes.id GROUP BY likes.id"
        results = connectToMySQL(cls.db).query_db(query)
        x=[]
        for i in results:
            proj_data = {
                "id" : i["id"],
                "name" : i["name"],
                "description" : i["description"],
                "git" : i["git"],
                "path" : i["path"],
                "url" : i["url"],
                "like" : {"id": i["likes.id"],"count": i['likes_count']}
            }
            x.append( proj_data )
        return x
    
    @classmethod
    def select_all(cls):
        query="SELECT *, count(users_likes.user_id) AS likes_count FROM projects JOIN likes ON likes.id = projects.like_id LEFT JOIN users_likes ON users_likes.like_id = likes.id GROUP BY likes.id"
        results = connectToMySQL(cls.db).query_db(query)
        x=[]
        for i in results:
            proj_data = {
                "id" : i["id"],
                "name" : i["name"],
                "description" : i["description"],
                "git" : i["git"],
                "path" : i["path"],
                "url" : i["url"],
                "like" : {"id": i["likes.id"],"count": i['likes_count']}
            }
            x.append( cls(proj_data) )
        return x
    
    @classmethod
    def insert(cls, data):
        query = "INSERT INTO projects(id, name, description, like_id, git, path, url) VALUES(%(id)s, %(name)s, %(description)s, %(like_id)s, %(git)s, %(path)s, %(url)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def insert_category(cls, data):
        q = "SELECT * FROM categories WHERE name=%(name)s"
        r = connectToMySQL(cls.db).query_db(q, data)
        print("#######insert_category########")
        if r:
            print(r)
            return r[0]['id']
        else:
            print("inserted")
            query= "INSERT INTO categories(name) VALUES(%(name)s)"
            return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def insert_cat_proj(cls, data):
        query="INSERT INTO projects_categories(category_id, project_id) VALUES(%(category_id)s, %(project_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)