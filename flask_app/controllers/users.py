from flask import Flask, render_template, request, redirect, get_flashed_messages, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_app.models.product import Product
from flask_app.models.like import Like
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

'''HOME'''
@app.route("/")
def index():
    likes=Like.select_all()
    return render_template("index.html", likes = likes)

'''LOGIN / REGISTER'''
@app.route("/login")
def login_reg():
    return render_template("log_reg.html")

@app.route("/login/process", methods=["POST"])
def login_process():
    data=request.form
    if not User.validate_login(data):
        return redirect("/login")
    else:
        session["logged_in"] = User.get_stars_email(data)
        print(session)
        return redirect("/dashboard")

@app.route("/register/process", methods=["POST"])
def create_process():
    data={k:v for k,v in request.form.items()}
    if not User.validate_insert(data):
        return redirect("/login")
    else:
        print(data)
        data["password"] = bcrypt.generate_password_hash(request.form['password'])
        User.insert(data)
        session["logged_in"] = User.get_stars_email(data)
        return redirect("/dashboard")

'''LOGOUT'''
@app.route("/logout")
def logout_process():
    session.clear()
    return redirect("/")

'''DASHBOARD'''
@app.route("/dashboard")
def dashboard():
    if session["logged_in"]["id"] == 1:
        u = session['logged_in']
        recieved = Message.read_recieved(u)
        sent = Message.read_sent(u)
        users = User.select_all()
        user = User.select_one(u)
        likes = Like.select_all()
        return render_template("dash.html", recieved=recieved, sent=sent, admin=True, users=users, user=user, likes=likes)
    else:
        u = session['logged_in']
        recieved = Message.read_recieved(u)
        sent = Message.read_sent(u)
        user = User.select_one(u)
        products = Product.check_product_user(u)
        user_likes = Like.select_by_user(u)
        likes = Like.select_all()
        return render_template("dash.html", recieved=recieved, sent=sent, user=user, products=products, user_likes=user_likes, likes=likes)

'''UPDATE'''
@app.route("/user/update")
def edit_show():
    data={"id" : session['logged_in']['id']}
    result = User.select_one(data)
    return render_template("edit.html", output=result)

@app.route("/user/update/process", methods=["POST"])
def edit_process():
    data={k:v for k,v in request.form.items()}
    if not User.validate_update(data):
        return redirect(f"/user/update/{data['id']}") 
    else:
        if data["new_pass"]:
            data["password"] = bcrypt.generate_password_hash(data["new_pass"])
            User.update(data)
        else:
            data["password"] = bcrypt.generate_password_hash(data["password"])
            User.update(data)
        return redirect(f"/user/read/{data['id']}")

'''CATCHALL'''
@app.route("/", defaults={"path":""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("catchall.html")