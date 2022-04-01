from flask import Flask, render_template, request, redirect, session, get_flashed_messages, jsonify
from flask_app import app
from flask_app.models.like import Like
from flask_app.models.like import User

@app.route("/like/create/process", methods=["POST"])
def like_create():
    data = request.form
    Like.insert(data)
    return redirect("/dashboard")

@app.route("/user_like/create", methods=["POST"])
def like_user_create():
    if session:
    # 1) if in session can like
        data={
            "like_id" : request.form["like_id"],
            "user_id": session['logged_in']['id']
            }
        # 2) use session and form for data dict
        if Like.validate_insert(data):
        # 3) validate user hasn't already liked
            Like.insert_like_user(data)
            # 4) insert user like
            new_stars=User.get_stars({"id" : session["logged_in"]["id"]})
            # 5) get the updated stars using session
            session["logged_in"] = new_stars
            # 6) update logged in stars
            return redirect(f"{request.form['url']}")
            # go back to url
        else:
        # 3) user has already liked
            return redirect(f"{request.form['url']}")
            # go back to url
    return redirect("/login")
    # 1) else redirect to login

@app.route("/user_like/<id>/delete")
def delete_user_like(id):
    data={"id":id, "user_id":session["logged_in"]["id"]}
    if session["logged_in"]["stars"] > 0:
        Like.delete_user_likes_stars(data)
        new_stars=User.get_stars({"id" : session["logged_in"]["id"]})
        session["logged_in"] = new_stars
        return redirect("/dashboard")
    else:
        Like.delete_user_likes(data)
        return redirect("/dashboard")

@app.route("/like/form", methods=["POST"])
def test_Form():
    if session:
        data={
            "like_id" : request.form["like_id"],
            "user_id": session['logged_in']['id']
        }
        if Like.validate_insert(data):
            Like.insert_like_user(data)
            new_stars=User.get_stars({"id" : session["logged_in"]["id"]})
            session["logged_in"] = new_stars
            like=Like.select_one({"id": request.form["like_id"]})
            return jsonify(stars = session["logged_in"]["stars"], num=like.count)
        else:
            return jsonify(message="not logged in")
    else:
        return jsonify(message="not logged in")