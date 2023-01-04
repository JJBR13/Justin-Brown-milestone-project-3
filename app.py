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
            else:
                # incorrect password
                flash("Incorrect Gamer Id and/or Password")
                return redirect(url_for("login"))

        else:
            # incorrect username
            flash("Incorrect Gamer Id and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # CHANGE TO FALSE BEFORE SUBMITTING!!!!!! <----
            debug=True)
