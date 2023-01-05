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
    categories = mongo.db.categories.find()
    console = mongo.db.console.find()
    return render_template(
        "index.html", categories=categories, console=console)


@app.route("/import_reviews")
def import_reviews():
    reviews = mongo.db.reviews.find()
    return render_template("reviews.html", reviews=reviews)


@app.route("/sign_up", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # checking user exits
        existing_gamer = mongo.db.gamer_id.find_one(
            {"gamer_id": request.form.get("gamer_id").lower()})

        if existing_gamer:
            flash("Sorry this gamer Id has been taken")
            return redirect(url_for("register"))

        register = {
            "gamer_id": request.form.get("gamer_id").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }

        # insert user to db
        mongo.db.gamer_id.insert_one(register)

        # user into session (cookie)
        session["gamer"] = request.form.get("gamerId").lower()
        flash("Gamer Registration Complete")
        return redirect(url_for("account", gamer_id=session["user"]))
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
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
    # getting gamers session gamer_id of db
    gamer_id = mongo.db.gamer_id.find_one(
        {"gamer_id": session["gamer"]})["gamer_id"]

    if session['gamer']:
        return render_template("account.html", gamer_id=gamer_id)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("See you soon")
    session.pop("gamer")
    return redirect(url_for("home"))


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # CHANGE TO FALSE BEFORE SUBMITTING!!!!!! <----
            debug=True)
