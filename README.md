# FoodWise
**FoodWise**  is a website developed from the idea of my journey as a parent to having to plan mealtimes that are heathly and tasty and been tested on families. FoodWise is a recipe sharing and management application where caregivers of children can create, share, edit and delete their ideas for recipes. 

I have designed the website to be user friendly as its main focus. It is designed to be fully responsive and accessible on a range of devices.  

**Link to website** [here](https://stran90.github.io/).

## Table Of Contents:
1. [Design & Planning](#design-&-planning)
    * [User Stories](#user-stories)
    * [Wireframes](#wireframes)
    * [Typography](#typography)
    * [Colour Scheme](#colour-scheme)
    * [Icons](icons)
    * [Database Diagram](#database-diagram)
    * [Features](#features)
    * [Future Implementations](#future-implementations)
    * [Accessabilty](#accesabilty)

2. [Technologies and Libraries Used](#technologies-used)

3. [Testing](#testing)
4. [Bugs](#bugs)
5. [Deployment](#deployment)
6. [Credits](#credits)
7. [Acknowledgment](#acknowledgment)

## Design & Planning:

### User Stories

- A parent/care giver looking for recipes not containing one or more of the top 14 common food allergens to cook for their family. 
- Any one looking for inspiration for a recipe to cook, that are free from top one or more of the top 14 food allergens. 

#### First-time Visitor Goals 
- As a first time user, I want to see short information about the main purpose of the site, how to use the site. 
- As a first time user, I want to look through recipes. 
- As a first time user, I want to be able create/login an user account. 

#### Registered User Visitor Goals
- As a registered user, I want to be able to add, edit and delete own recipes.  
- As a registered user, I want to be able to upload images to my recipes. 
- As a registered user, I want to be able to add recipes based on categories. 


### Wireframes
For all page wireframes, please see [WIREFRAMES.md](WIREFRAMES.md) file.

### Typography
- [Google Fonts](https://fonts.google.com/)

  - Used 'Roboto': "light 300" font for the website as it great for accessibility.

### Colour Scheme
<p align="center">
  <img src="static/images/readme/color-palette.png" width="50%" height="20%">
</p>

The website uses a contrast of colours, I wanted to choose colours to have good contrast and look professional, ensuring that the content is visually manageable for users. I used coolors to design my colour palette. 

### Icons

I opted to integrate Font Awesome into the project to make use of the wide range of icons available. 

I included a favicon in the project using Favicon.


![Favicon Screenshot](/static/images/favicon/favicon.ico)

### DataBase Diagram
The project employs a non-relational database model, which implies that each collection is not interconnected in the same way as in a relational database. Consequently, when a document in one collection required referencing a document in another collection, special handling was necessary. 

The project being a data-centric project, I aimed for a comprehensive planning phase concerning the data to be stored in the database, the interlinking of each document, and the user interaction on the frontend, encompassing complete CRUD operations. I documented detailed plans to guide the development of Python logic and relevant forms effectively.

#### Image of the database diagram for the project:

Users:

```
{
    _id: ObjectId,
    user_id: integer,
    f_name: "string",
    l_name: "string",
    email: "string",
    username: "string",
    password: "hashed password",
}
```

Recipes:

```
{
    _id: ObjectId
    recipe_name: "string",
    recipe_description: "string",
    category_name: "string"
    ingredients: [
        "Ingredient 1", 
        "Ingredient 2",
        "Ingredient 2",
    ],
    "preparations": [
        "Step 1",
        "Step 2", 
        "Step 3", 
    ],
    "cook _time": Integer,
    "serves": Integer,
    "created_by": username
    "image_url": "string"
}
```

Categories:

```
{
    "_id": ObjectId,
    "category_name": "string",
    "category_description": "string"
}
```

### Features:
The website is composed of 6 pages that is accessible from the navigation menu if user is signed in (home page, profile, categories, recipes, add recipes and logout page). The website also has a register, recipe description and 404 error page.

All pages on the website have:

-A responsive navigation bar at the top which allows the user to navigate through the site. 

-A footer

* Home Page. 
  * Hero Section. 
  The hero shows an image of fresh fruit and vegetables indicating health and wellness. 

* Profile Page. 
  * Card Section
  This gives users information the site has stored like first name, last name, email, and username. 

* Categories Page. 
  * This section gives user abilty to add/edit/delete categories. 
 
* Recipes Page. 
  * Recipe cards
  This section shows card panels of recipes that have been created by the user and others that have been added to the site. Users can view all recipes that have been added onto the site, including theirs. More information revealed by clicking on more (three vertical dots) icon on recipe card. A link to the full recipe page for user to view full information.  
  * Floating buttons. 
  Users have only the abilty to edit/delete their recipe card, floating button of edit/delete will be seen on the recipe card created by the user. There is also a floating button by the title page for user to add a recipe from the page.  

* Add Recipe Page. 
  * Add Recipe Form
  This section shows a from to fill in to add a recipe on the site. The form contains fields for the recipe name, description, ingredients, preparation, serves, cook time, category and optional upload of an image by user. The user submits the form using the submit button. Users must fill in the input fields to be able to submit the form. If they don't a tooltip will guide them to fill in any information they have missed. Ability to add an image if user wanter, however a stock image will be used. This page gives quick access to add a recipe rather than going through the recipes page. 

* Registration Page
  * Registration From 
  This section shows a from for the user to fill in, in order to use the website. The form consists of input fields for the users first name, last name, email, username, and choosen password and retype password field. There is a cancel button that redirects the user to the homepage, and a submit button to register. Flask message will appear if username and email have been used. Flask message seen if registration was successful and directs users to the login page. 
  
* Login Page. 
  * Log in Form
  This section shows a from to fill in login to the website. It contains email and password input fields. Flask messages will appear if email and password are incorrect. If correct email and password are entered the user is directed to the profile page and a welcome message of the user's name is shown. 

* Recipe Page. 
  * This shows full details of the recipe the user has choosen to view. Recipe name, description, ingredients, preparation, serves, cook time, category and who it was posted by can be seen.

* 404 Page. 
  * Found if the user navigates to a page that doesn't exist within the site 

### Future Implementations.

  * Add admin function so only admin can add/edit/delete categories and only admin have option to delete any recipe.  
  * Improve profile page, user can upload an image. 
  * Add latest recipes to the home page. 
  * Add a search function on the navbar. 
  * Comments section or like, users can interact with each other.
  * Make this site an allergy friendly, filter option to filter recipes that linked to the filtered allergens choosen. 
  * Direct photo upload from user, using cloudinary or similar technology. 

### Accessibility 

I have been mindful during coding to ensure the website is as accessible friendly as possible. I have achieved this by:

* Using semantic HTML.
* Using descriptive alt attributes on images on the site. 
* Ensuring there are sufficient colour contrast throughout the site.
* Using font style with good accessibility.


## Technologies Used
### Including Frameworks, Libraries & Programs Used
The table below displays the technologies and programming languages utilized in this project, along with their respective purposes within the project.


| Language/Technology | Use                                                                                                                                                                                                                |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HTML                | Used to build templates for all pages on site                                                                                                                                                                                          |
| CSS                 | Used to customise styling on all elements                                                                                                                                                                                  |
| Python              | Used for processing data between database and front end                                                                                                                                                     |
| MongoDB             | Data storage  users                                                                                                                                                                                                          |
| Flask               |  Micro web framework for Python that allows you to build web applications. logic                                                                                                                                                               |
| Jinja               | Templating engine for Pythons                                                                                                                                         |
| Werkzeug            | WSGI (Web Server Gateway Interface) utility library for Python present                                                                                                                                                                      |
| Gitpod        | Used as the main development environment                                                                                                                                                                                                                                                                                                                  |
| Git        | Used for version control within development environment                                                                                                                                                                      |
| GitHub        | Hosting service for software development and version control using Git, to save and store files for the website.  repo                                                                                                                                                                      |
| Balsamiq            | Used to create wireframes.dates                                                                                                                                        |
| Heroku              | Used to deploy the live site                                                                                                                                                                                                           |
| Materialize         | The Framework for the website. Code used for additional CSS styling was also implemented in style.css. 
| Google Fonts        | Used for site fonts; Courgette and Nunito                                                                                                                                                                                              |
| Am I Responsive?        | An online tool to check how responsive the website is on different devices. Screenshot generated by the tool is presented in about section of the README file.                                                                                                                                                                                  |
| FontAwesome        | Iconography on the website                                                                                                                                                                                                |
| Google Dev Tools             | To troubleshoot and test features, solve issues with responsiveness and styling. 
| Favicon        | Used for site favicon 
| Code Institute Python Linter    | Used to test the app.py file for Pep8 compliance                                                                                                                                                                                             |
W3 HTML Validator        | Used to test all HTML files                                                                                                                                                                                  |
| FW3 CSS Validator        | Used to test CSS file website                                                                                                                                                                                                |
| Lighthouse (Chrome)           | TUsed to audit the site for performance, quality, best practices and SEO. 

## Testing

For all manual user testing, lighthouse performance testing and code validation, please see [TESTING.md](TESTING.md) file.


## Bugs
During the development process, I used Google Chrome Devtools to manually test the features myself as I added them, following the user stories as I built the site and keeping a list of the bugs and their fixes along the way.

#### Fixed bugs

1. If user already signed in, redirects
        if "user" in session:
        flash("You are already signed in")
        return redirect(url_for("profile"))

User
File "/workspace/Foodwise-project3/app.py", line 126
    return redirect(url_for("profile"))
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: 'return' outside function.



2. Logout function immediately redirects to the login page, regardless of whether the user was logged in or not.

    - Fixed by modify the logout function to first check if the user is logged in before performing the logout actions. 

3. Bug where encrypted user ID in database was seen instead of username posted recipe card. 

    - changed session["user"] to username. 

4. Bug found where users could edit or delete other users recipes from the liked recipe section of their profile page.

    - Fixed by adding in the missing jinja if statement around the edit and delete buttons.

7. Bug found where category selection was not rendering categories from database. 

    - Fixed by changing the route link category_name instead of category_Id

8. Bug found when the user can look at the categories page edit/delete on the page when not logged in. 

    - Added functionality for if 'user' not session to edit, add category and categories routes.

9. Bug found, categoty selection not updating or being added to the recipe. 

    - ensuring all routes and links corresponded to the database collection and name needed. Checked for wrong given expressions in app.py and htmls.

## Deployment
This website is deployed to Heroku from a GitHub repository.

#### Creating Repository on GitHub
* Log into GitHub and locate the repository.
* At the top locate the settings option. 
* Scroll towards the bottom of the page and locate GitHub Pages
* Click on the link "Check it out here!"
* Under 'Source' dropdown, click 'Master' from the options.
* Click the save button.
* The site is now published, it may not be available immediately.
* The site URL is visible on the green bar under the "Github Pages".

#### Gitpod
For website deployment I have decided to go with [Gitpod](https://gitpod.io) because it provides fast website load speeds, simple configuration setup and very easy deployment process.

- From the dashboard create new "Project",
- Login with GitHub,
- Import desired git repository,
- Configure project,
- Type "python3 app.py" into terminal 
- Select 'Open in new browser' when pop up appears. 
- Website deployed!

#### Making a Local Clone
To clone the FoodWise repository:

1. Log in (or sign up) to GitHub.
2. Go to the repository for this project, https://github.com/STRAN90/Foodwise-project3.git
3. Click on the code button, select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown.
4. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory.
5. Type 'git clone' into the terminal and then paste the link you copied in step 3. Press enter.

### Local deployment 

#### Forking the Github Repository 
To fork this repo, follow the below step by step instructions:

1. Navigate to the [GitHub Repository](https://github.com/STRAN90/Foodwise-project3.git) for this project.
2. Click `Fork` button in top right under main navigation bar.
3. A copy of this repo should now exist in your GitHub account. for this project.
2. Click `Fork` button in top right under main navigation bar.
3. A copy of this repo should now exist in your GitHub account.

#### Creating an app on Heroku
- After creating the repository on GitHub, head over to [heroku](https://www.heroku.com/) and sign in.
- On the home page, click **New** and **Create new app** from the drop down.
- Give the app a name(this must be unique) and select a **region** I chose **Europe** as I am in Europe, Then click **Create app**.

#### Deploying to Heroku.

To deploy your app on [Heroku](https://www.heroku.com/platform), these are the steps to follow: 

1. Register for an account on Heroku to begin.
2. Click on the "New" button and choose "Create New App."
3. Pick a unique name for your app.
4. Select a region for deployment and click on "Create App."
5. Choose your preferred connection method.
6. Ensure your GitHub profile is visible and search for your repository. You might need to link your GitHub account if not done during registration.
7. Once your repository is located, click on "Connect."
8. Go to the "Settings" tab and select "Reveal Config Vars."
9. Add each variable from your env.py file as key-value pairs here without quotes. For example, key = PORT and value = 5000.
10. After adding all config vars, return to the "Deploy" tab and enable "Automatic Deploys." 
11. Choose the branch to deploy and click "Deploy."
12. Once deployment is complete, click "Open App" to view your live site.

| Key | Value
|:-------:|:--------|
| DATABASE_URL  |    |
| IP  |    |
|  PORT |    |
|  SECRET_KEY   |     |

Actual Enviroment variables not disclosed for security

## Credits

- Tesco for their supply of recipes to use on this site when developing [Tesco Real Food](https://realfood.tesco.com/recipes)
- [Code insitute](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+NRDB_L5+2/courseware/9e2f12f5584e48acb3c29e9b0d7cc4fe/054c3813e82e4195b5a4d8cd8a99ebaa/) Mini walkthrough project. 

###  Media

- [Freepik](https://www.freepik.com/) - was used for background image and stock image used for recipe.  
- [Coolors](https://coolors.co/) - for colour palette used in this README.md

### Acknowledgments

- My mentor Rohit Sharma for his knowledge and helpful advice. 
- Google search engine for limitless resources about web development. 