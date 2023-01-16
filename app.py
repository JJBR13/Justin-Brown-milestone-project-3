import os
from flask import (
    Flask, render_template,
    flash, redirect, request, session, url_for)
from flask_pymongo import PyMongo
# Allows objects to be taken from DB
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


if os.path.exists("env.py"):
    import env


app = Flask(__name__)

# linking to db
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    """
    Renders home page when lauching the main site.
    """
    categories = mongo.db.categories.find().sort("category_name", 1)
    console = mongo.db.console.find().sort("console_type", 1)
    return render_template(
        "index.html", categories=categories, console=console)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    """
    Allows user to search review content
    and titles in the database.
    """
    reviews = list()
    reviews = list(mongo.db.reviews.find({"$text": {"$search": query}}))
    return render_template("reviews.html", reviews=reviews)


@app.route("/import_reviews")
def import_reviews():
    """
    GET 's all reviews from db,
    displaying them on review.html.
    """
    reviews = mongo.db.reviews.find()
    return render_template("reviews.html", reviews=reviews)


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """
    Sign-up page, allows user to register, if username
    doesnt already exist
    """
    if request.method == "POST":
        # checking user exits
        existing_gamer = mongo.db.gamer_id.find_one(
            {"gamer_id": request.form.get("gamer_id")})

        # checks varible return to sign_up
        if existing_gamer:
            flash("Sorry this gamer Id has been taken")
            return redirect(url_for("sign_up"))

        # Dictionary created from form data to insert new gamer_id
        sign_up = {
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "gamer_id": request.form.get("gamer_id").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }

        # insert user to db
        mongo.db.gamer_id.insert_one(sign_up)

        # user into session (cookie)
        session["gamer"] = request.form.get("gamer_id")
        flash("Gamer Registration Complete")

        return render_template('account.html', gamer_id=session['gamer'])

    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Allows exsiting user to log into account.
    Checks user agaisnt db data, allowing login.
    Redirects to account page.
    """
    if request.method == "POST":
        # check gamer id exists
        existing_gamer = mongo.db.gamer_id.find_one(
            {"gamer_id": request.form.get("gamer_id").lower()})

        if existing_gamer:
            # match hash pasword to input password
            if check_password_hash(
               existing_gamer["password"], request.form.get("password")):
                session["gamer"] = request.form.get("gamer_id").lower()
                flash("WELCOME BACK, {}".format(
                        request.form.get("gamer_id")))
                return redirect(url_for(
                    "account", gamer_id=session["gamer"]))
            else:
                # incorrect password
                flash("Incorrect Gamer Id and/or Password")
                return redirect(url_for("login"))

        else:
            # incorrect username
            flash("Incorrect Gamer Id and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/account/<gamer_id>", methods=["GET", "POST"])
def account(gamer_id):
    """
    Passes gamer session gamer_id from db,
    returns them to account page.
    Where all reviews created via the user are displayed.
    """
    # getting gamers session gamer_id of db
    gamer_id = mongo.db.gamer_id.find_one(
        {"gamer_id": session["gamer"]})["gamer_id"]

    if session['gamer']:
        reviews = list(mongo.db.reviews.find(
            {"uploaded_by": session["gamer"]}))
        return render_template(
            "account.html", gamer_id=gamer_id, reviews=reviews)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    Removes logged in session gamer cookie,
    Redirects them to home page.
    """
    flash("See you soon")
    session.pop("gamer")
    return redirect(url_for("home"))


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    """
    Allows gamer to create review, add to the db.
    Gets values from Db, renders add_review.html.
    """
    if request.method == "POST":
        review = {
            "console_type": request.form.get("console_type"),
            "game_name": request.form.get("game_name"),
            "category_type": request.form.get("category_type"),
            "review_content": request.form.get("review_content"),
            "uploaded_by": session["gamer"]
        }
        mongo.db.reviews.insert_one(review)
        flash("THANK YOU FOR THE REVIEW ON: {}".format(
            request.form.get("game_name")))
        return redirect(url_for("home"))

    console = mongo.db.console.find().sort("console_type", 1)
    categories = mongo.db.categories.find()
    return render_template(
        "add_review.html", console=console, categories=categories)


@app.route("/edit_review/<reviews_id>", methods=["GET", "POST"])
def edit_review(reviews_id):
    """
    Allows gamer to edit review, displays flash message if sucessfull.
    Redirects gamer to account page.
    """
    # If session is active
    if session.get("gamer"):
        review = mongo.db.reviews.find_one_or_404(
            {"_id": ObjectId(reviews_id)})
        # If session user owns the post
        if review["uploaded_by"] == session["gamer"]:
            if request.method == "POST":
                save = {
                    "console_type": request.form.get("console_type"),
                    "game_name": request.form.get("game_name"),
                    "category_type": request.form.get("category_name"),
                    "review_content": request.form.get("review_content"),
                    "uploaded_by": session["gamer"]
                }
                # Update saved to mongoDB
                mongo.db.reviews.update_one(
                    {"_id": ObjectId(reviews_id)}, {"$set": save})
                flash("Your review has been changed")
                # get the user, then need to get the id for a redirect
                user = mongo.db.gamer_id.find_one(
                    {"gamer_id": session["gamer"]})
                return redirect(url_for("account", gamer_id=user['_id']))

            reviews = mongo.db.reviews.find_one({"_id": ObjectId(reviews_id)})
            console = mongo.db.console.find().sort("console_type", 1)
            categories = mongo.db.categories.find().sort("category_name", 1)
            return render_template(
                "edit_review.html",
                reviews=reviews, console=console, categories=categories)
        else:
            # Displays if user is loggged in but as wrong user.
            flash(
                "Your logged in as the incorrect user to edit this review")
            return redirect(url_for("home"))
    # Displays when no user is logged in
    flash("Your not authorise to edit this review")
    return redirect(url_for("home"))


@app.route("/delete_review/<reviews_id>")
def delete_review(reviews_id):
    """
    Enables gamer to delete review, they created.
    Redirects them back to account page.
    """
    # If session is active
    if session.get("gamer"):
        review = mongo.db.reviews.find_one_or_404(
            {"_id": ObjectId(reviews_id)})
        # If session user owns the post
        if review["uploaded_by"] == session["gamer"]:
            # get the review, delete this after
            review = mongo.db.reviews.find_one({"_id": ObjectId(reviews_id)})
            # get the user, we need to get the id for a redirect
            user = mongo.db.gamer_id.find_one({"gamer_id": session["gamer"]})

            if review["uploaded_by"] == session["gamer"]:
                if review:
                    # try to delete review here
                    mongo.db.reviews.delete_one({"_id": ObjectId(reviews_id)})
                    # success message
                    flash("Review Sucessfully Deleted")
                    # redirect
                    return redirect(url_for("account", gamer_id=user['_id']))
                else:
                    # review does not exist, redirect to home
                    flash("This review does not exist")
                    return redirect(url_for("account", gamer_id=user['_id']))
        # Displays if logged in as wrong user
        else:
            flash("Your logged in as the incorrect user to delete this review")
            return redirect(url_for("home"))
    # Displays when no user is logged in
    flash("Your not authorise to edit this review")
    return redirect(url_for("home"))


@app.route("/contact")
def contact():
    """
    Renders contact.html
    """
    return render_template('contact.html')


@app.route("/read_more/<reviews_id>")
def read_more(reviews_id):
    """
    Gets review '_id' from Db, returns relavant review
    in read_more.html
    """
    # get reviews_id from Db
    review = mongo.db.reviews.find_one({"_id": ObjectId(reviews_id)})

    return render_template('read_more.html', review=review)


@app.errorhandler(404)
def not_found(error):
    """
    Returns 404.html, if 404 error is present.
    """
    # Redirect for route handle error
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def not_found(error):
    """
    Returns 505.html, if server error is present.
    """
    # Redirect for route handle error
    return render_template('505.html', error=error), 505


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # CHANGE TO FALSE BEFORE SUBMITTING!!!!!! <----
            debug=False)
