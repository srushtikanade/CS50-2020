import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import time

from helpers import  login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///proj.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("apology.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("LOGGED IN!")

        # Redirect user to home page
        return redirect("/")



    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    """Register user"""
    if request.method== "GET":
        return render_template("register.html")

    else:
        users=db.execute("SELECT * FROM users WHERE username=:username",
        username=request.form.get("username"))

         # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", issue=" Enter username")


        #Ensure username is unique
        elif len(users)>0:

            return render_template("apology.html", issue=" Enter unique username")


        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html",issue=" Enter password")

        elif not (request.form.get("password")).isupper:
            return render_template("apology.html" ,issue=" Enter only lowercase")

        elif  (request.form.get("password")).isdigit():
            return render_template("apology.html" ,issue=" Enter no digits")


        elif request.form.get("password")!=request.form.get("c_password"):
             return render_template("apology.html",issue=" Entered passwords must match each other")


        # Query database for username
        return_value=db.execute("INSERT INTO users(username,hash) VALUES(:username,:hash)", username=request.form.get("username"),hash=generate_password_hash(request.form.get("password")))

        flash("REGISTERED!")
        return redirect("/login")

@app.route("/thoughts", methods=["GET", "POST"])
@login_required
def thoughts():
    if request.method=="GET":
        return render_template("thoughts.html")

    else:
        db.execute("INSERT INTO ideas(idea,user_id,time) VALUES(:idea,:user_id,date()) ",
        user_id=session["user_id"],
        idea=request.form.get("thoughts"))


        flash("YOU JUST POSTED YOUR THOUGHT")



        return redirect("/")

@app.route("/")
@login_required
def index():
    
    users=db.execute("SELECT * FROM users WHERE id=:user_id",
    user_id=session["user_id"])

    thoughts=db.execute("SELECT * FROM ideas WHERE user_id=:user_id ORDER BY time DESC LIMIT 5",
    user_id=session["user_id"])

    tasks=db.execute("SELECT * FROM planner WHERE user_id=:user_id ORDER BY time DESC LIMIT 5" ,
    user_id=session["user_id"])

    cards=db.execute("SELECT * FROM cards WHERE user_id=:user_id ORDER BY time DESC LIMIT 5" ,
    user_id=session["user_id"])


    return render_template("index.html",thoughts=thoughts,tasks=tasks,cards=cards,users=users)
    
    
   

@app.route("/planner", methods=["GET", "POST"])
@login_required
def planner():

    if request.method=="GET":

        return render_template("planner.html")

    else:
        db.execute("INSERT INTO planner(task,user_id,time) VALUES(:task,:user_id,time()) ",
        user_id=session["user_id"],
        task=request.form.get("task"))


        flash("YOU JUST ADDED A TASK!")



        return redirect("/")

@app.route("/cards", methods=["GET", "POST"])
@login_required
def cards():
    if request.method=="GET":
        return render_template("cards.html")

    else:
        db.execute("INSERT INTO cards(topic,question,answer,user_id,time) VALUES(:topic,:question,:answer,:user_id,date()) ",
        topic=request.form.get("topic"),
        question=request.form.get("question"),
        answer=request.form.get("answer"),
        user_id=session["user_id"])



        flash("YOU JUST ADDED A CARD!")



        return redirect("/")

@app.route("/history")
@login_required
def history():
    thoughts=db.execute("SELECT * FROM ideas WHERE user_id=:user_id ORDER BY time DESC",
    user_id=session["user_id"])

    tasks=db.execute("SELECT * FROM planner WHERE user_id=:user_id ORDER BY time DESC" ,
    user_id=session["user_id"])

    cards=db.execute("SELECT * FROM cards WHERE user_id=:user_id ORDER BY topic ASC",
    user_id=session["user_id"])


    return render_template("index.html",thoughts=thoughts,tasks=tasks,cards=cards)

@app.route("/pomodoro")
@login_required
def pomodoro():
    return render_template("pomodoro.html")

@app.route("/stat")
@login_required
def stat():
    return render_template("stat.html")

@app.route("/changepw",methods=["GET","POST"])
@login_required
def changepw():
    if request.method=="GET":
        return render_template("changepw.html")

    else:
        user=db.execute("SELECT hash FROM users WHERE id=:user_id",
        user_id=session["user_id"])
        if not request.form.get("oldpw") or request.form.get("newpw") or request.form.get("c_newpw"):
            return render_template("apology.html",issue="Please enter password")

        elif check_password_hash((user[0]["hash"]),request.form.get("oldpw")):
            return render_template("apology.html",issue="password does not match")

        elif request.form.get("newpw")!=request.form.get("c_newpw"):
            return render_template("apology.html",issue="password does not match")

        else:
            db.execute("UPDATE users SET hash=:hash WHERE id=:user_id",
            hash=generate_password_hash(request.form.get("newpw")),
            user_id=session["user_id"])

            flash("CHANGED PASSWORD!")

            return redirect("/")

@app.route("/changename",methods=["GET","POST"])
@login_required
def changename():
    if request.method=="GET":
        return render_template("changename.html")

    else:
        username=request.form.get("newname")
        users=db.execute("SELECT username FROM users WHERE username=:username",
        username=username)

        if not request.form.get("oldname") or request.form.get("newname") or request.form.get("c_newname"):
            return render_template("apology.html",issue="Please enter username")


        elif request.form.get("newname")!=request.form.get("c_newname"):
            return render_template("apology.html",issue="usernames do not match")

        elif len(users)>0:
            return render_template("apology.html",issue="username must be unique")

        else:
            db.execute("UPDATE users SET username=:username WHERE id=:user_id",
            username=username,
            user_id=session["user_id"])

            flash("CHANGED USERNAME!")

            return redirect("/")




# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
