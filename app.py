import os
from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_records")
def get_records():
    records = mongo.db.records.find()
    return render_template("records.html", records=records)


# Show details for selected record
@app.route("/show_record/<record_id>")
def show_record(record_id):
    record = mongo.db.records.find_one({"_id": ObjectId(record_id)})
    return render_template("show_record.html", record = record)



# Registration based on the task manager walkthrough project
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username_taken = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if username_taken:
            flash("This username is not available. Please try another.")
            return render_template("register.html")
        register_user = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register_user)

        session["session_user"] = request.form.get("username").lower()
        flash("You've been registered. Welcome!")
        return redirect(url_for("show_profile", username = session["session_user"]))
    return render_template("register.html")


# Login based on the task manager walkthrough project
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        user_exists = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if user_exists:
            if check_password_hash(
                    user_exists["password"], request.form.get("password")):
                    session["session_user"] = request.form.get("username").lower()
                    flash("Welcome back{}".format(request.form.get("username")))
                    return redirect(url_for(
                        "show_profile", username = session["session_user"]))   
            else:
                flash("The username or password you entered is not correct. Please try again.")
                return redirect(url_for("login"))
        else:
            flash("The username or password you entered is not correct. Please try again.")
            return redirect(url_for("login"))

    return render_template("login.html")

# Profile page based on task manager walkthrough
@app.route("/profile/<username>", methods=["GET", "POST"])
def show_profile(username):
    username = mongo.db.users.find_one(
        {"username": session["session_user"]})["username"]
    if session["session_user"]:
        return render_template("profile.html", username = username)
    return redirect(url_for("login"))

'''@app.route("/profile/<username>", methods = ["GET", "POST"])
def show_profile(username):
    if not session["session_user"]:
        return redirect(url_for("login.html"))
    else: 
        username = mongo.db.users.find_one(
        {"username": session["session_user"]})["username"]
        return render_template("profile.html", username = username)
'''
@app.route("/logout")
def logout():
    flash("Goodbye. You have been logged out.")
    session.pop("session_user")
    return redirect (url_for("login"))


@app.route("/add_record", methods = ["GET","POST"])
def add_record():
    if request.method == "POST":
        added_date = datetime.now()
        record = {
            "common_name": request.form.get("common_name"),
            "botanical_name": request.form.get("botanical_name"),
            "experience": request.form.get("experience"),
            "summer": request.form.get("summer"),
            "winter": request.form.get("winter"),
            "added_by": session["session_user"],
            "added_date": added_date, 
            "image_link": request.form.get("image_url")   
        }
        mongo.db.records.insert_one(record)
        flash("Record added. Thanks for your contribution.")
        return redirect(url_for("get_records"))
    return render_template("add_record.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
