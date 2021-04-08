import os
from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
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


@app.route("/profile/<username>")
def show_profile(username):
    username = mongo.db.users.find_one(
        {"username": session['session_user']})["username"]
    return render_template("profile.html", username = username)





if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
