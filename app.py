import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import abort
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
    """ Adds current user if signed in """
    user = None
    if "user" in session:
        user = get_user(session["user"])
    return render_template("home.html", recipes=recipes, user=user)


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        flash("You are already registered and signed in.")
        return redirect(url_for("profile"))

    if request.method == "POST":
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        password_check = request.form.get("password_check")

        """ Input validation """
        if not all([f_name, l_name, email, username, password, password_check]):
            flash("All fields are required.")
            return redirect(url_for("register"))
        elif password != password_check:
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        existing_user = mongo.db.users.find_one({"username": username})
        existing_email = mongo.db.users.find_one({"email": email})

        if existing_user or existing_email:
            flash("Username or email already exists.")
            return redirect(url_for("register")) 
        elif password != password_check:
            flash("Username or email already exists.")
            return redirect(url_for("register")) 
        else:
            hashed_password = generate_password_hash(password)
            user_data = {
                "f_name": f_name,
                "l_name": l_name,
                "email": email,
                "username": username,
                "password": hashed_password
            }
            mongo.db.users.insert_one(user_data)
            flash("Registration successful!", "success")
            return redirect(url_for("login"))  # Redirect to login page after successful registration

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        """ Redirect to profile page if user is already signed in """
        flash("You are already signed in.", "info")
        return redirect(url_for("profile"))

    if request.method == "POST":
        """ Retrieve email and password from the form """
        email = request.form.get("email")
        password = request.form.get("password")

        if not all([email, password]):
            flash("Email and password are required.", "error")
            return redirect(url_for("login"))

        """ Check if email exists in database """
        existing_user = mongo.db.users.find_one({"email": email})

        if existing_user and check_password_hash(existing_user["password"], password):
            """ Password matches user input, log in the user """
            session["user"] = existing_user["email"] 
            flash(f"Welcome {existing_user['f_name']} {existing_user['l_name']}", "success")
            return redirect(url_for("profile"))
            """ Invalid password match """
            flash("Incorrect Email and/or Password", "error")
            return redirect(url_for("login"))

        """ Email or password invalid """
        flash("Incorrect Email and/or Password", "error")
        return redirect(url_for("login"))
        flash("Incorrect email and/or password.", "error")
        return redirect(url_for("login"))

    """ Render the login page for GET requests """
    return render_template("login.html")


@app.route("/logout")
def logout():
    """ Check if "user" key exists in the session"""
    if "user" in session:
        """ Remove user from session cookie """
        session.pop("user")
        flash("You have been logged out", "sucess")
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
    try:
        recipes = list(mongo.db.recipes.find())

        if "user" in session:
            user = mongo.db.users.find_one({"user_id": session["user"]})
            return render_template("recipes.html", recipes=recipes, user=user)

        return render_template("recipes.html", recipes=recipes)

    except Exception as e:
        """ Handle database errors or other exceptions """
        flash("Error fetching recipes. Please try again later.", "error")
        app.logger.error(f"Error fetching recipes: {str(e)}")
        return redirect(url_for("home"))  

@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if "user" not in session:
        flash("You need to be logged in to add a recipe", "error")
        return redirect(url_for("login"))

    user_email = session["user"]
    user = mongo.db.users.find_one({"email": user_email})
    username = user["username"]
    
    categories = mongo.db.categories.find()
    
    if request.method == "POST":
        recipe_name = request.form.get("recipe_name")
        recipe_description = request.form.get("recipe_description")
        ingredients = request.form.getlist("ingredients")
        preparation = request.form.getlist("preparation")
        serves = int(request.form.get("serve"))
        cook_time = int(request.form.get("cook_time"))
        category_id = request.form.get("category_id")
        image_url = request.form.get("image_url")

        if not recipe_name or not recipe_description or not ingredients or not preparation:
            flash("All fields are required.", "error")
        else:
            recipe = {
                "recipe_name": recipe_name,
                "recipe_description": recipe_description,
                "ingredients": ingredients,
                "preparation": preparation,
                "serves": serves,
                "cook_time": cook_time,
                "category_id": category_id,
                "created_by": user_email,
                "image_url": image_url
            }

            try:
                mongo.db.recipes.insert_one(recipe)
                flash("Recipe added successfully.", "success")
                return redirect(url_for("recipes"))
            except Exception as e:
                flash(f"An error occurred: {e}", "error")

    return render_template("add_recipe.html", categories=categories)




@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if "user" not in session:
        flash("You need to be logged in to edit a recipe", "error")
        return redirect(url_for("login"))

    user_email = session["user"]

    try:
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        if not recipe:
            flash("Recipe not found for editing", "error")
            return redirect(url_for("recipes"))

        created_by = recipe.get("created_by")

        if created_by != user_email:
            flash("You are not authorized to edit this recipe", "error")
            return redirect(url_for("recipes"))
            
        categories = mongo.db.categories.find()
        
        if request.method == "POST":
            """ Get form data """
            recipe_name = request.form.get("recipe_name")
            recipe_description = request.form.get("recipe_description")
            ingredients = request.form.get("ingredients")
            preparation = request.form.get("preparation")
            serves = int(request.form.get("serve"))
            cook_time = int(request.form.get("cook_time"))
            category_id = request.form.get("category_id")
            image_url= request.form.get("image_url")


            """ Check for empty or invalid fields """
            if not all([recipe_name, recipe_description, ingredients, preparation, serves, cook_time,]):
                flash("All fields are required.", "error")
            else:
                """ Update recipe object """
                updated_recipe = {
                    "recipe_name": recipe_name,
                    "recipe_description": recipe_description,
                    "ingredients": ingredients,
                    "preparation": preparation,
                    "serves": serves,
                    "cook_time": cook_time,
                    "category_id": category_id,
                    "image_url": image_url,
                }

                """ Update the recipe in the database """
                mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$set": updated_recipe})
                flash("Recipe updated successfully.", "success")
                return redirect(url_for("recipes"))
        
        return render_template("edit_recipe.html", categories=categories, recipe=recipe)
    except InvalidId:
        flash("Invalid recipe ID.", "error")
        return redirect(url_for("recipes"))
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for("recipes"))
        

@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    if "user" not in session:
        flash("You need to be logged in to delete a recipe", "error")
        return redirect(url_for("login"))

    user_email = session["user"]

    try:
        # Find the recipe and its creator
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        if not recipe:
            flash("Recipe not found for deletion", "error")
            return redirect(url_for("recipes"))

        created_by = recipe.get("created_by")

        if created_by != user_email:
            flash("You are not authorized to delete this recipe", "error")
            return redirect(url_for("recipes"))

        # Attempt to delete the recipe
        result = mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
        if result.deleted_count == 1:
            flash("Recipe successfully deleted", "success")
        else:
            flash("Recipe not found for deletion", "error")
    except Exception as e:
        flash(f"Error deleting recipe: {str(e)}", "error")

    return redirect(url_for("recipes"))
    
@app.route("/recipe_description/<recipe_id>", methods=["GET", "POST"])
def recipe_description(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if "user" in session:
        user = mongo.db.users.find_one({"user_id": session["user"]})
        return render_template("recipe_description.html", recipe=recipe, user=user)

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
            "category_name": request.form.get("category_id"),
            "category_description": request.form.get("category_description"),
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

@app.route("/delete_category/<category_id>", methods=["GET", "POST"])
def delete_category(category_id):
    mongo.db.categories.delete_one({"_id": ObjectId(category_id)})

    flash("Category successfully deleted", "success")
    return redirect(url_for("categories"))  # Redirect to categories list page


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)