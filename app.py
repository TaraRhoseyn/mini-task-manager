import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

# installing instance of Flask:
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# CONSTRUCTOR METHOD TO SETUP INSTANCE OF PYMONGO
mongo = PyMongo(app)


@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks = mongo.db.tasks.find()
    # grabs tasks from 'tasks' collection
    # and assigns them to the 'tasks' variable on L22 >
    return render_template("tasks.html", tasks=tasks)



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db:
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            # redirecting user if username already taken:
            return redirect(url_for("register"))

        register = { # actions as 'else' if no existing user is found
            "username": request.form.get("username").lower(), # dictionary items to store in DB
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register) # inserting dict as variable to db

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration successfull!")

    return render_template("register.html")


# telling app how & where to run app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
