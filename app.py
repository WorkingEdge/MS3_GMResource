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

#Home page, default index
@app.route("/")
@app.route("/get_records")
def get_records():
    records = mongo.db.records.find()
    return render_template("records.html", records=records)


# Show details for selected record
@app.route("/show_record/<record_id>", methods=["GET", "POST"])
def show_record(record_id):
    record = mongo.db.records.find_one({"_id": ObjectId(record_id)})
    #return render_template("show_record.html", record = record)    
    if request.method == "POST":
        comment_date = datetime.now()
        commenter_id = mongo.db.users.find_one(
        {"username": session["session_user"]})["_id"]
        mongo.db.records.update(
            {"_id": ObjectId(record_id)},
            {"$push": 
                {"comments":
                    {
                    "comment_by": session["session_user"],
                    "comment_text": request.form.get("comment_text"),
                    "comment_date": comment_date,
                    "commenter_id": commenter_id
                }
            }
        }
        )
        flash("Comment added. Thanks for your contribution.")
        return redirect(url_for("show_record", record_id = record_id))
    return render_template("show_record.html", record = record)


# Edit record
@app.route("/edit_record/<record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    record = mongo.db.records.find_one({"_id": ObjectId(record_id)})    
    
    if request.method == "POST":
        updated_date = datetime.now()
        common_name = request.form.get("common_name").lower()
        user_id = mongo.db.users.find_one(
        {"username": session["session_user"]})["_id"]
        # Perform search to check if the entry exists in any product. Store this info as well
        contained_in = list(mongo.db.products.find(
        {"contains_common": common_name }))
        #Iterate over the returned list to get the product name (for embed) and product id (for reference by ObjectId)
        products = []
        for product in contained_in:
            product_name = product.get("prod_name")
            products.append(product_name)
        product_ids = []
        for product in contained_in:
            product_id = product.get("_id")
            product_ids.append(product_id)
        #Create the object that will be inserted in the db
        updated_record = {
            "title": request.form.get("record_title"),
            "common_name": common_name,
            "botanical_name": request.form.get("botanical_name"),
            "experience": request.form.get("experience"),
            "summer": request.form.get("summer"),
            "winter": request.form.get("winter"),
            "added_by": session["session_user"],
            "user_id": user_id,
            "updated_date": updated_date, 
            "image_link": request.form.get("image_url"),
            "contained_in": products,
            "contained_in_ids": product_ids
        }
        mongo.db.records.update({"_id": ObjectId(record_id)}, {"$set": updated_record})
        flash("Record updated. Thanks for your contribution.")
        return redirect(url_for("show_record", record_id = record_id))
    return render_template("edit_record.html", record = record)

# Delete record 
@app.route("/delete_record/<record_id>", methods=["POST"])
def delete_record(record_id):
    mongo.db.records.remove({"_id": ObjectId(record_id)})
    flash("The record has been deleted.")
    return redirect(url_for('show_profile', username = session['session_user']))


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
    user_id = mongo.db.users.find_one(
        {"username": session["session_user"]})["_id"]
    records = list(mongo.db.records.find(
        {"user_id": user_id }))
    commented = list(mongo.db.records.find(
        {"comments":{"$elemMatch": {"commenter_id": user_id}}}))
    for post in commented:
        comment_details = []

    if session["session_user"]:
        return render_template("profile.html", username = username, records = records)
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("Goodbye. You have been logged out.")
    session.pop("session_user")
    return redirect (url_for("login"))


@app.route("/add_record", methods = ["GET","POST"])
def add_record():
    if request.method == "POST":
        #Variables to hold data to store on db
        added_date = datetime.now()
        common_name = request.form.get("common_name").lower()
        user_id = mongo.db.users.find_one(
        {"username": session["session_user"]})["_id"]
        # Perform search to check if the entry exists in any product. Store this info as well
        contained_in = list(mongo.db.products.find(
        {"contains_common": common_name }))
        #Iterate over the returned list to get the product name (for embed) and product id (for reference by ObjectId)
        products = []
        for product in contained_in:
            product_name = product.get("prod_name")
            products.append(product_name)
        product_ids = []
        for product in contained_in:
            product_id = product.get("_id")
            product_ids.append(product_id)
        #Create the object that will be inserted in the db
        record = {
            "title": request.form.get("record_title"),
            "common_name": common_name,
            "botanical_name": request.form.get("botanical_name"),
            "experience": request.form.get("experience"),
            "summer": request.form.get("summer"),
            "winter": request.form.get("winter"),
            "added_by": session["session_user"],
            "user_id": user_id,
            "added_date": added_date, 
            "image_link": request.form.get("image_url"),
            "contained_in": products,
            "contained_in_ids": product_ids
        }
        mongo.db.records.insert_one(record)
        flash("Record added. Thanks for your contribution.")
        return redirect(url_for("get_records"))
    return render_template("add_record.html")


@app.route("/products")
def show_products():
    products = list(mongo.db.products.find())
    return render_template("products.html", products = products)

@app.route("/add_product", methods = ["GET","POST"])
def add_product():
    if request.method == "POST":
        #Variables to hold data to store on db
        added_date = datetime.now()
        common_names = request.form.get("common_names").lower().split(", ")
        user_id = mongo.db.users.find_one(
        {"username": session["session_user"]})["_id"]
        #Create the object that will be inserted in the db
        product = {
            "prod_name": request.form.get("product_name"),
            "contains_common": common_names,
            "botanical_names": request.form.get("botanical_names"),
            "summer": request.form.get("summer"),
            "winter": request.form.get("winter"),
            "n_fixing": request.form.get("winter"),
            "added_by": session["session_user"],
            "user_id": user_id,
            "added_date": added_date, 
            "image_link": request.form.get("image_url"),
            "prod_notes": request.form.get("prod_notes"),
            "prod_price": request.form.get("prod_price")
        }
        mongo.db.products.insert_one(product)
        flash("Product added.")
        return redirect(url_for("show_products"))
    return render_template("add_product.html")


# Delete product 
@app.route("/delete_product/<product_id>", methods=["POST"])
def delete_product(product_id):
    mongo.db.products.remove({"_id": ObjectId(product_id)})
    flash("The product has been deleted.")
    return redirect(url_for('show_products'))

# Edit product
@app.route("/edit_product/<product_id>", methods = ["GET","POST"])
def edit_product(product_id):
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if request.method == "POST":
        #Variables to hold data to store on db
        updated_date = datetime.now()
        common_names = request.form.get("common_names").lower().split(", ")
        user_id = mongo.db.users.find_one(
        {"username": session["session_user"]})["_id"]
        #Create the object that will be inserted in the db
        updated_product = {
            "prod_name": request.form.get("product_name"),
            "contains_common": common_names,
            "botanical_names": request.form.get("botanical_names"),
            "summer": request.form.get("summer"),
            "winter": request.form.get("winter"),
            "n_fixing": request.form.get("winter"),
            "added_by": session["session_user"],
            "user_id": user_id,
            "image_link": request.form.get("image_url"),
            "prod_notes": request.form.get("prod_notes"),
            "prod_price": request.form.get("prod_price"),
            "updated_date": updated_date
        }
        mongo.db.products.update({"_id": ObjectId(product_id)}, {"$set": updated_product})
        flash("Product updated.")
        return redirect(url_for("show_products"))
    return render_template("edit_product.html", product = product)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
