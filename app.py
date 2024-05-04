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


def get_user(user_id):
    # Function to retrieve user information from the database based on user_id
    user = mongo.db.users.find_one({"user_id": user_id})
    return user


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
                session["user"] = existing_user["email"]  # Storing email for simplicity
                flash("Welcome, {}".format(existing_user["email"]), "success")
                return redirect(url_for("profile"))  # Redirect to profile without passing username

            # Invalid password match
            flash("Incorrect Email and/or Password", "error")
            return redirect(url_for("login"))

        # Email doesn't exist
        flash("Incorrect Email and/or Password", "error")
        return redirect(url_for("login"))

    # Check if user is signed in
    if "user" in session:
        # Redirect to profile page if signed in
        flash("You are already signed in", "info")
        return redirect(url_for("profile"))

    # Render the login page if not signed in
    return render_template("login.html")


@app.route("/logout")
def logout():
    # Check if "user" key exists in the session
    if "user" in session:
        # Remove user from session cookie
        session.pop("user")
        flash("You have been logged out", "info")
    else:
        flash("You are not logged in", "error")

    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    # Check if "user" key exists in the session
    if "user" in session:
        # Get user data from the database based on the email stored in the session
        user_email = session["user"]
        user = mongo.db.users.find_one({"email": user_email})

        if user:
            # Render the profile template and pass the user data
            return render_template("profile.html", user=user)
        else:
            flash("User not found", "error")
            return redirect(url_for("login"))
    else:
        flash("Please log in to view this page", "error")
        return redirect(url_for("login"))


@app.route("/recipes")
def recipes():
    recipes = mongo.db.recipes.find()
    # adds current user if signed in
    if "user" in session:
        user = mongo.db.users.find_one({"user_id": session["user"]})
        return render_template("recipes.html", recipes=recipes, user=user)

    return render_template("recipes.html", recipes=recipes)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
       if "user" in session:
        user = get_user(session["user"])
        
        if request.method == "POST":
            # Get form data
            recipe_name = request.form.get("recipe_name")
            recipe_description = request.form.get("recipe_description")
            ingredients = request.form.getlist("ingredients")
            preparation = request.form.getlist("preparation")
            serves = int(request.form.get("serve"))
            cook_time = int(request.form.get("cook_time"))

            # Check for empty or invalid fields
            if not recipe_name or not recipe_description or not ingredients or not preparation:
                flash("All fields are required.", "error")
            else:
                # Create recipe object
                recipe = {
                    "recipe_name": recipe_name,
                    "recipe_description": recipe_description,
                    "ingredients": ingredients,
                    "preparation": preparation,
                    "serves": serves,
                    "cook_time": cook_time,
                }

                # Insert the recipe into the database
                mongo.db.recipes.insert_one(recipe)
                flash("Recipe added successfully.", "success")
                return redirect(url_for("recipes"))  # Redirect to recipe list page
                
        return render_template("add_recipe.html")


@app.route("/edit_recipe")
def edit_recipe():
    return render_template("edit_recipe.html")


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})

    flash("Recipe successfully deleted")
    return redirect(url_for("recipes"))

@app.route("/recipe_description/<recipe_id>", methods=["GET", "POST"])
def recipe_description(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if "user" in session:
        user = mongo.db.users.find_one({"user_id": session["user"]})
        return render_template("recipe_description.html", recipe=recipe, user=user)

    return render_template("recipe_description.html", recipe=recipe)

@app.route("/categories")
def categories():
    categories = mongo.db.categories.find()
    if "user" in session:
        user = get_user(session["user"])
        return render_template("categories.html", categories=categories, user=user)
    else:
        # Handle case where user is not logged in
        return render_template("categories.html", categories=categories, user=None)

@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name"),
            "category_description": request.form.get("category_description"),
            "category_color": request.form.get("category_color")
        }
        mongo.db.categories.insert_one(category)
        flash("New category added!")
        return redirect(url_for("categories"))

    if "user" in session:
        user = get_user(session["user"])
        return render_template("add_category.html", user=user)

    return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        # Updates the category in the db
        edit = {
            "category_name": request.form.get("category_name"),
            "category_description": request.form.get("category_description"),
            "category_color": request.form.get("category_color")
        }
        mongo.db.categories.update_one({"_id": ObjectId(category_id)}, {
            "$set": edit})
        # Updates the category on all applicable recipes in recipe db
        query = {
            "categories._id": ObjectId(category_id)
            }
        update = {"$set": {
                "categories.$.category_name":
                request.form.get("category_name"),
                "categories.$.category_description":
                request.form.get("category_description"), 
                "categories.$.category_color":
                request.form.get("category_color")}}

        mongo.db.recipe.update_many(query, update)

        flash("Category successfully updated")
        return redirect(url_for("categories"))

    if "user" in session:
        user = get_user(session["user"])
        category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
        return render_template("edit_category.html", category=category, user=user)

    return render_template("edit_category.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)