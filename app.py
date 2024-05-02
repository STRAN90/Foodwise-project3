import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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
@app.route("/home")
def home():
    recipes = list(mongo.db.recipes.find())
    # adds current user if signed in
    if session:
        user = mongo.db.users.find_one({"user_id": session["user"]})
        return render_template("home.html", recipes=recipes, user=user)

    return render_template("home.html", recipes=recipes)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
    
        # check if username already exists in db and reloads page until user info is all valid
    
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if existing_user and existing_email:
            flash("Username and email already exist")
            return redirect(url_for("register"))
        elif existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        elif existing_email:
            flash("Email already exists")
            return redirect(url_for("register"))
        elif request.form.get("password") != request.form.get(
                "password_check"):
            flash("Passwords do not match")
            return redirect(url_for("register"))
        else:
            
            # unique id to new user 
            user_id = 1
            existing_id = True
            while existing_id:
                if user_id not in mongo.db.used_ids.find_one({"name": "used_ids"})["ids"]:
                    existing_id = False
                    break
                else:
                    user_id += 1

            mongo.db.used_ids.update_one({"name": "used_ids"}, {
                "$push": {"ids": user_id}})

            # builds new user dict with default superuser and admin permissions
            new_user = {
                "user_id": user_id,
                "f_name": request.form.get("f_name").capitalize(),
                "l_name": request.form.get("l_name").capitalize(),
                "email": request.form.get("email"),
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                    request.form.get("password")),
                "is_super": False,
                "is_admin": False}
            mongo.db.users.insert_one(new_user)

            # puts new user id into session cookie
            session["user"] = user_id
            flash("Successfully Registered!")
            return redirect(url_for("profile"))


    if "user" in session:
        flash("You are already registered")
        return redirect(url_for("profile"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if email exists in db
        existing_user = mongo.db.users.find_one({"email": request.form.get("email")})

        if existing_user:
            # Ensure password matches user input
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("email")
                flash("Welcome, {}".format(request.form.get("email")))
                return redirect(url_for("profile"), username=session["user"])
            else:
                # Invalid password match
                flash("Incorrect Email and/or Password")
                return redirect(url_for("login"))
        else:
            # Email doesn't exist
            flash("Incorrect Email and/or Password")
            return redirect(url_for("login"))

    # Check if user is signed in
    if "user" in session:
        # Redirect to profile page if signed in
        flash("You are already signed in")
        return redirect(url_for("profile"))

    # Render the login page if not signed in
    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))

@app.route("/profile")
def profile():
    # Check if user is logged in
    if "user" not in session:
        flash("Please log in to view this page")
        return redirect(url_for("login"))

    # Pull current user from database using id from session cookie
    user_id = session["user"]
    user = mongo.db.users.find_one({"user_id": user_id})

    if user:
        return render_template("profile.html", user=user)
    else:
        flash("User not found")
        return redirect(url_for("login"))



@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/add_recipe")
def add_recipe():
    return render_template("add_recipe.html")


@app.route("/edit_recipe")
def edit_recipe():
    return render_template("edit_recipe.html")

@app.route("/categories")
def categories():
    return render_template("categories.html")

@app.route("/add_category")
def add_category():
    return render_template("add_category.html")


@app.route("/edit_category")
def edit_category():
    return render_template("edit_category.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)