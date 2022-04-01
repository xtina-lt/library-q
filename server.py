from flask_app import app
# 1) import flask application initiated in __init__.py

from flask_app.controllers import users, replies, projects, products, messages, likes
# 2) import routes

if __name__ == "__main__":
    app.run(debug=True)
    #3) if in file