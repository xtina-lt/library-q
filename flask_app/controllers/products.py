from flask import Flask, render_template, request, redirect, session, get_flashed_messages, jsonify
from flask_app import app


from flask_app.models.like import Like
from flask_app.models.product import Product
from flask_app.models.user import User

@app.route("/gifshop")
def gifshop():
    if session:
        return render_template("gifshop.html", output=Product.select_all())
    else:
        return redirect("/login")

@app.route("/product/create", methods=["POST"])
def product_create():
    like_data={
        "description": request.form["description"],
        "url": "/gifshop",
    }
    print(like_data)
    new_like = Like.insert(like_data)
    product_data={k:v for k,v in request.form.items()}
    product_data["like_id"] = new_like
    print(product_data)
    Product.insert(product_data)
    return redirect("/gifshop")

@app.route("/user_products/create", methods=["POST"])
def user_products_create():
    if session:
        data={k:v for k,v in request.form.items()}
        data["cost"] = int(data["cost"])
        if not Product.check_product_user(data):
            if Product.validate_product_buy(data["cost"]):
                Product.user_products_create(data)
                Product.product_user_stars(data)
                session["logged_in"] = User.get_stars({"id":session["logged_in"]["id"]})
                return redirect("/dashboard")
            else:
                return redirect("/gifshop")
        else:
            return redirect("/gifshop")
    else:
        return redirect("/login")
    