import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
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
    """Route function for the home page. Retrieves the current
    user if signed in and renders the home page.
    """
    user = None
    if "user" in session:
        user = get_user(session["user"])
    return render_template("home.html", user=user)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Route function for the register page. Handles user registration.
    Handles both displaying and processing user registration forms,
    ensuring valid user information by checking for existing usernames
    and emails in the users' collection and verifying password matches.
    Displays appropriate flashed messages and reloads the page until
    all user information is validated.
    """
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
                "password": hashed_password,
            }
            mongo.db.users.insert_one(user_data)
            flash("Registration successful!", "success")
            return redirect(
                url_for("login")
            )  # Redirect to login page after successful registration

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Route function for user login. Manages both displaying and
    processing user login forms. Checks if the user is already
    signed in, retrieves email and password from the form, checks
    for existing email in the database, and verifies password matches.
    Logs in the user if credentials are correct and redirects to the
    profile page. Displays appropriate flashed messages for success or failure.
    """
    if "user" in session:
        # Redirect to profile page if user is already signed in
        flash("You are already signed in.", "info")
        return redirect(url_for("profile"))

    if request.method == "POST":
        # Retrieve email and password from the form
        email = request.form.get("email")
        password = request.form.get("password")

        if not all([email, password]):
            flash("Email and password are required.", "error")
            return redirect(url_for("login"))

        """ Check if email exists in database """
        existing_user = mongo.db.users.find_one({"email": email})

        if existing_user and check_password_hash(existing_user["password"], password):
            """Password matches user input, log in the user"""
            session["user"] = existing_user["email"]
            flash(
                f"Welcome {existing_user['f_name']} {existing_user['l_name']}",
                "success",
            )
            return redirect(url_for("profile"))
            """ Invalid password match """
            flash("Incorrect Email and/or Password", "error")
            return redirect(url_for("login"))

        """ Email or password invalid """
        flash("Incorrect Email and/or Password", "error")
        return redirect(url_for("login"))
        flash("Incorrect email and/or password.", "error")
        return redirect(url_for("login"))

    # Render the login page for GET requests
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Route function for user logout. Checks if the user is logged
    in by verifying the presence of the "user" key in the session.
    Removes the user from the session cookie upon logout and displays
    an appropriate flashed message. Redirects to the login page after
    logout.
    """
    # Check if "user" key exists in the session
    if "user" in session:
        # Remove user from session cookie
        session.pop("user")
        flash("You have been logged out", "sucess")
    else:
        flash("You are not logged in", "error")

    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    """Route function for user profile page. Checks if the user is logged
    in by verifying the presence of the "user" key in the session. Retrieves
    user data from the database based on the email stored in the session.
    Renders the profile template with the user data if the user is found.
    Displays appropriate flashed messages and redirects to the login page if
    authentication fails.
    """
    # Check if "user" key exists in the session
    if "user" in session:
        # Get user data from the database
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
    """Route function to display recipes. Retrieves recipes from
    the database and renders the recipes page. If a user is logged
    in, also retrieves user information for the session
    """
    try:
        recipes = list(mongo.db.recipes.find())

        if "user" in session:
            user = mongo.db.users.find_one({"user_id": session["user"]})
            return render_template("recipes.html", recipes=recipes, user=user)

        return render_template("recipes.html", recipes=recipes)

    except Exception as e:
        # Handle database errors or other exceptions
        flash("Error fetching recipes. Please try again later.", "error")
        app.logger.error(f"Error fetching recipes: {str(e)}")
        return redirect(url_for("home"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """Route function to add a new recipe. Allows logged-in users
    to add a new recipe, validates input data, and saves the recipe
    to the database. If the user is not logged in, redirects to the
    login page with an error message.
    """
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
        category_name = request.form.get("category_name")
        image_url = request.form.get("image_url")

        if not (recipe_name and recipe_description and ingredients and preparation):
            flash("All fields are required.", "error")
        else:
            # Check if the selected category name exists in the categories collection
            category = mongo.db.categories.find_one({"category_name": category_name})

            if category:
                recipe = {
                    "recipe_name": recipe_name,
                    "recipe_description": recipe_description,
                    "ingredients": ingredients,
                    "preparation": preparation,
                    "serves": serves,
                    "cook_time": cook_time,
                    "category_name": category_name,
                    "created_by": user_email,
                    "image_url": image_url,
                }

                try:
                    mongo.db.recipes.insert_one(recipe)
                    flash("Recipe added successfully.", "success")
                    return redirect(url_for("recipes"))
                except Exception as e:
                    flash(f"An error occurred: {e}", "error")
            else:
                flash("Invalid category selected.", "error")

    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """Route function to edit a recipe."""
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
            # Retrieve form data
            recipe_data = {
                "recipe_name": request.form.get("recipe_name"),
                "recipe_description": request.form.get("recipe_description"),
                "ingredients": request.form.get("ingredients"),
                "preparation": request.form.get("preparation"),
                "serves": int(request.form.get("serve")),
                "cook_time": int(request.form.get("cook_time")),
                "category_name": request.form.get(
                    "category_name"
                ),  # Updated category name
                "image_url": request.form.get("image_url"),
                "created_by": user_email,  # Ensure ownership remains unchanged
            }

            # Check for empty or invalid fields
            if not all(recipe_data.values()):
                flash("All fields are required.", "error")
            else:
                # Update the recipe in the database
                mongo.db.recipes.update_one(
                    {"_id": ObjectId(recipe_id)}, {"$set": recipe_data}
                )
                flash("Recipe updated successfully.", "success")
                return redirect(url_for("recipes"))

        return render_template("edit_recipe.html", categories=categories, recipe=recipe)
    except (InvalidId, ValueError):
        flash("Invalid recipe ID or invalid data.", "error")
    except Exception as e:
        flash(f"An error occurred: {e}", "error")

    return redirect(url_for("recipes"))


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    """Route function to delete a recipe. Allows logged-in users
    to delete their own recipes. Checks authentication, verifies
    recipe ownership, and deletes the recipe from the database.
    """
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
    """Route function to display recipe details. Retrieves the
    details of a specific recipe from the database based on its ID.
    If a user is logged in, also retrieves user information
    for the session.
    """
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    if "user" in session:
        user = mongo.db.users.find_one({"user_id": session["user"]})
        return render_template("recipe_description.html", recipe=recipe, user=user)
    else:
        flash("Please log in to view this page", "error")
        return redirect(url_for("login"))


@app.route("/categories")
def categories():
    """Route function to display categories. Retrieves categories
    from the database and renders the categories page. If a user is
    logged in, retrieves user information for the session. Otherwise,
    redirects to the login page.
    """
    if "user" not in session:
        # Redirect non-logged-in users to the login page
        return redirect(url_for("login"))

    categories = mongo.db.categories.find()
    user = get_user(session["user"])
    return render_template("categories.html", categories=categories, user=user)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    """Route function to add a new category. Allows logged-in
    users to add a new category to the database. Retrieves form
    data for category creation and inserts the new category into
    the database.
    """
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name"),
            "category_description": request.form.get("category_description"),
        }
        mongo.db.categories.insert_one(category)
        flash("New category added!")
        return redirect(url_for("categories"))

    if "user" in session:
        user = get_user(session["user"])
        return render_template("add_category.html", user=user)
    else:
        flash("Please log in to view this page", "error")
        return redirect(url_for("login"))

    return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    """Route function to edit a category. Allows logged-in users
    to edit an existing category in the database. Retrieves form data
    for category editing and updates the category details in the database.
    Also updates the category details in all applicable recipes in the
    recipes database.
    """
    if request.method == "POST":
        # Updates the category in the db
        edit = {
            "category_name": request.form.get("category_name"),
            "category_description": request.form.get("category_description"),
        }
        mongo.db.categories.update_one({"_id": ObjectId(category_id)}, {"$set": edit})
        # Updates the category on all applicable recipes in recipe db
        query = {"categories._id": ObjectId(category_id)}
        update = {
            "$set": {
                "categories.$.category_name": request.form.get("category_name"),
                "categories.$.category_description": request.form.get(
                    "category_description"
                ),
            }
        }

        mongo.db.recipe.update_many(query, update)

        flash("Category successfully updated")
        return redirect(url_for("categories"))

    if "user" in session:
        user = get_user(session["user"])
        category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
        return render_template("edit_category.html", category=category, user=user)
    else:
        flash("Please log in to view this page", "error")
        return redirect(url_for("login"))

    return render_template("edit_category.html")


@app.route("/delete_category/<category_id>", methods=["GET", "POST"])
def delete_category(category_id):
    """Route function to delete a category. Allows logged-in users
    to delete an existing category from the database. Deletes the
    category based on the provided category ID.
    """
    if "user" not in session:
        flash("You need to be logged in to delete a category", "error")
        return redirect(url_for("login"))

    mongo.db.categories.delete_one({"_id": ObjectId(category_id)})

    flash("Category successfully deleted", "success")
    return redirect(url_for("categories"))


@app.errorhandler(404)
def page_not_found(e):
    """Error handler for 404 Not Found. Renders a custom 404 error
    page when a page is not found.
    """
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
