import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import time

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")



# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():


    users = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

    stocks=db.execute("SELECT symbol,n_share,price_of_share FROM transactions WHERE user_id=:user_id GROUP BY symbol",user_id=session["user_id"])

    shares={}

    for stock in stocks:
        shares[stock["symbol"]]=lookup(stock["symbol"])

    cash_left=users[0]["cash"]

    total=cash_left

    return render_template("index.html",stocks=stocks,shares=shares,total=total,cash_left=cash_left,)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    """Buy shares of stock"""
    if request.method== "GET":
        return render_template("buy.html")


    else:
        stock=lookup(request.form.get("symbol"))

        if not stock:

            return apology("must provide the correct symbol", 403)

        try:
            n_share=int(request.form.get("n_share"))
        except:
            return apology("must be positive number of shares",403)

        if n_share<=0:
            return apology("must be positive number of shares",403)

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash_left=rows[0]["cash"]
        price_of_share=stock["price"]

        total_price=price_of_share*n_share

        if total_price>cash_left:

            return apology("not adequate funds",403)


        db.execute("UPDATE users SET cash=cash- :price WHERE id=:user_id", price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id,symbol,n_share,price_of_share) VALUES(:user_id,:symbol,:n_share,:price_of_share)",
        user_id=session["user_id"],
        symbol=stock["symbol"],
        n_share=request.form.get("n_share"),
        price_of_share=stock["price"])

        flash("BOUGHT!")

        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks=db.execute("SELECT symbol,n_share,price_of_share,action,time FROM transactions WHERE user_id=:user_id",
    user_id=session["user_id"])

    return render_template("history.html",stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        stock=lookup(request.form.get("symbol"))
        if stock==None:
            return apology("must provide the correct symbol", 403)

        return render_template("quoted.html", stock=stock)


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    """Register user"""
    if request.method== "GET":
        return render_template("register.html")

    else:
         # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not (request.form.get("password")).isupper:
            return apology("only lowercase",403)

        elif not (request.form.get("password")).isdigit():
            return apology("must contain digit",403)


        elif request.form.get("password")!=request.form.get("c_password"):
             return apology("must provide same password", 403)


        # Query database for username
        return_value=db.execute("INSERT INTO users(username,hash) VALUES(:username,:hash)", username=request.form.get("username"),hash=generate_password_hash(request.form.get("password")))

        return redirect("/login")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method=="GET":

        return render_template("sell.html")

    else:
        stock=lookup(request.form.get("symbol"))
        n_share_sell= int(request.form.get("shares"))


        if stock==None:
            return apology("must provide correct symbol",403)

        elif n_share_sell<=0 :



            return apology("must provide positive number of shares",403)

        else:

            users=db.execute("SELECT cash FROM users WHERE id=:user_id",user_id=session["user_id"])
            shares=db.execute("SELECT SUM(n_share) as total_shares FROM transactions WHERE user_id=:user_id AND symbol=:symbol GROUP BY symbol",
            user_id=session["user_id"],
            symbol=request.form.get("symbol"))

            if shares[0]["total_shares"]<n_share_sell:

                return apology("You cannot sell more than you own",403)

            else:
                price_of_share=stock["price"]

                total_price=price_of_share*n_share_sell

                db.execute("UPDATE users SET cash=cash+:price WHERE id=:user_id",
                price=total_price,
                user_id=session["user_id"])

                db.execute("INSERT INTO transactions (user_id,symbol,n_share,price_of_share,time) VALUES(:user_id,:symbol,:n_share,:price_of_share,time())",
                    user_id=session["user_id"],
                    symbol=request.form.get("symbol"),
                    n_share=shares[0]["total_shares"]-n_share_sell,
                    price_of_share=price_of_share)

            flash("SOLD!")

            return redirect("/")



@app.route("/add",methods=["GET","POST"])
@login_required
def add():
    if request.method=="GET":
        return render_template("add.html")

    else:
        amount=request.form.get("amount")
        if not amount:
            return apology("please enter amount",403)


        else:
            db.execute("UPDATE users SET cash=cash+:amount WHERE id=:user_id",
            amount=amount,
            user_id=session["user_id"])

            return redirect("/")


@app.route("/changepw",methods=["GET","POST"])
@login_required
def changepw():
    if request.method=="GET":
        return render_template("changepw.html")

    else:
        user=db.execute("SELECT hash FROM users WHERE id=:user_id",
        user_id=session["user_id"])
        if not request.form.get("oldpw") or request.form.get("newpw") or request.form.get("c_newpw"):
            return apology("Please enter password",403)

        elif check_password_hash((user[0]["hash"]),request.form.get("oldpw")):
            return apology("password does not match",403)

        elif request.form.get("newpw")!=request.form.get("c_newpw"):
            return apology("password does not match",403)

        else:
            db.execute("UPDATE users SET hash=:hash WHERE id=:user_id",
            hash=generate_password_hash(request.form.get("newpw")),
            user_id=session["user_id"])

            flash("CHANGED!")

            return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
