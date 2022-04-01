from flask import Flask, render_template, request, redirect, session, jsonify
from flask_app import app
from flask_app.models.user import User
from flask_app.models.like import Like
from flask_app.models.message import Message
from flask_app.models.product import Product

@app.route("/message/create", methods=["POST"])
def message_create():
    like_data={
        "description": request.form["content"],
        "url" : "/dashboard",
    }
    like_id = Like.insert(like_data)
    # 1) create a like for message like button
    data = {k:v for k,v in request.form.items()}
    data["like_id"] = like_id
    Message.create(data)
    # 2) create a message
    return redirect("/dashboard")

@app.route("/message/update", methods=["POST"])
def message_update_process():
    data = request.form
    Message.update(data)
    return jsonify(message=data['content'])

@app.route("/message/<message_id>/<like_id>/delete")
def message_delete(message_id, like_id):
    data={
        "message_id" : message_id,
        "like_id" : like_id
    }
    Like.delete(data)
    Message.delete(data)
    return redirect("/dashboard")

