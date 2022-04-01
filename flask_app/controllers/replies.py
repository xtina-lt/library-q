from flask import Flask, render_template, request, redirect, session, jsonify
from flask_app import app
from flask_app.models.like import Like
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_app.models.reply import Reply

@app.route("/reply/create", methods=["POST"])
def reply_create():
    print("###REPLY CREATE###")
    like_data ={
        "description" : request.form["content"],
        "url" : "/dashboard"
    }
    like_id = Like.insert(like_data)
    print(like_data)
    data = {k:v for k,v in request.form.items()}
    data["like_id"] = like_id
    print(data)
    Reply.create(data)
    return redirect("/dashboard")

@app.route("/reply/<reply_id>/update")
def dashboard_edit_reply(reply_id):
    if session['logged_in']['id'] == 1:
        u = session['logged_in']
        user = User.select_one(u)
        users = User.select_all()
        likes = Like.select_all()
        recieved = Message.read_recieved(u)
        sent = Message.read_sent(u)
        return render_template("dash.html", users = users, user = user, likes = likes, recieved = recieved, sent = sent, edit = int(reply_id), edit_type="reply")
    elif session['logged_in']:
        u = session['logged_in']
        user = User.select_one(u)
        user_likes = Like.select_by_user(u)
        recieved = Message.read_recieved(u)
        sent = Message.read_sent(u)
        likes = Like.select_all()
        return render_template("dash.html", user = user, user_likes = user_likes, likes = likes, recieved = recieved, sent = sent, edit = int(reply_id), edit_type="reply")
    else:
        return redirect("/login")

@app.route("/reply/update", methods=["POST"])
def reply_update_process():
    print("##########")
    data = request.form
    print(data)
    Reply.update(data)
    return jsonify(message=data['content'])

# @app.route("/reply/update", methods=["POST"])
# def reply_update_process():
#     data = request.form
#     print("##REPLY UPDATE##")
#     print(data)
#     Reply.update(data)
#     return redirect("/dashboard")

@app.route("/reply/<reply_id>/<like_id>/delete")
def reply_delete(reply_id, like_id):
    data={
        "reply_id" : reply_id,
        "like_id" : like_id
    }
    Like.delete(data)
    Reply.delete(data)
    return redirect("/dashboard")
