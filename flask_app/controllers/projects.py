import requests
from flask import Flask, render_template, request, redirect, session
from flask_app import app
from flask_app.models.project import Project
from flask_app.models.like import Like

''''READ PROJECTS'''
@app.route("/projects")
def select_all_projects():
    results = Project.select_all()
    return render_template("projects.html", output = results)

'''CREATE PROJECT'''
@app.route("/projects/fetch")
def select_projects_py():
    db_projects = Project.select_all_json()
    db_values= [v for d in db_projects for v in d.values()]
    response = requests.get('https://api.github.com/users/xtina-lt/repos')
    response = response.json()
    results= []
    for i in response:
        if i["id"] in db_values:
            continue
        else:
            topics = ", ".join(i["topics"])
            data={
                "id" : i["id"],
                "name" : i["name"].replace("-", " ").replace("_", " "),
                "language" : i["language"],
                "description" : i["description"],
                "categories": topics,
                "git": i["html_url"],
                "url" : i["homepage"],
            }
            results.append(data)
    return render_template("projects_pyfetch.html", output = results)

@app.route("/project/create", methods=["POST"])
def project_create():
    data = {k:v for k,v in request.form.items()}
    # 1) get form items
    like = {"description": data["name"], "url": f"/project/{data['id']}"}
    data["like_id"]=Like.insert(like)
    # 2) create like and add to data
    data["path"] = f"/project/{data['id']}"
    # 3) create path and add to data
    project_id = Project.insert(data)
    # 4) create project
    c = data["categories"].split(', ')
    categories = [{"name": i} for i in c]
    categories.append({"name": data['language']})
    print(categories)
    # 5) get categories and split into a list
    cat_list = []
    if categories:
        for i in categories:
            result = Project.insert_category(i)
            # 6 ) insert, or skip category if in db already
            cat_list.append({'project_id':data['id'], 'category_id': result})
        for i in cat_list:
            Project.insert_cat_proj(i)
    return redirect("/projects/fetch")





