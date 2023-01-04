import os
from flask import (
    Flask, render_template,
    flash, redirect, session, url_for)
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
    return render_template("index.html", categories=categories)


@app.route("/sign_up", methods=["GET", "POST"])
def register():
    return render_template("sign_up.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # CHANGE TO FALSE BEFORE SUBMITTING!!!!!! <----
            debug=True)
