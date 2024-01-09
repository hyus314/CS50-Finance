import os
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, jsonify, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)
# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute(
        "SELECT name, shares FROM stocks JOIN portfolios on stocks.id = portfolios.stock_id WHERE portfolios.user_id = ?", session["user_id"]
        )
    user_rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    data = []

    user_info = {"cash": int(user_rows[0]["cash"]), "total": float(user_rows[0]["cash"])}

    for row in rows:
        stock = lookup(row["name"])
        data.append({
                "symbol": row["name"], "shares": row["shares"], "price": stock["price"], "total": format(stock["price"] * row["shares"], '.2f')
                })
        calculation_result = float(stock["price"]) * int(row["shares"])
        user_info["total"] = user_info.get("total", 0) + calculation_result

    user_info["cash"] = format(user_info["cash"], '.2f')
    user_info["total"] = format(user_info["total"], '.2f')
    return render_template('index.html', message=request.args.get('message'), data=data, user_info=user_info)


@app.route("/stocks", methods=["GET"])
@login_required
def stocks():
    rows = db.execute("SELECT name, shares FROM stocks JOIN portfolios on stocks.id = portfolios.stock_id WHERE portfolios.user_id = ?", session["user_id"])
    return json.dumps({"data": rows})

@app.route("/shares")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")

    # get form input
    symbol = request.form.get("symbol")
    shares = int(request.form.get("shares"))

    # get stock from lookup
    stock = lookup(symbol)

    # validate form input
    if not symbol:
        return apology("please input symbol")
    if stock == None:
        return apology("stock does not exist")
    if shares == 0:
        return apology("cannot buy 0 shares")
    if shares < 0:
        return apology("cannot buy negative shares")

    # transaction begin
    # initializing variables for transaction

    user_funds = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    stock_price = stock['price']
    transaction_sum = shares * stock_price
    if user_funds < transaction_sum:
        return apology("insufficient funds")
    else: # if the transaction can proceed successfully, we continue on to register the transaction in the portfolio of the user

        # first we check if the user has bought this stock before, we begin with checking if that stock exists in the database
        # if the stock does not exist in the database, we are sure that the user has not bought such stock.
        # if otherwise, we still do not know if the user has that portfolio with the stock in the database, so we check again

        stock_rows = db.execute("SELECT id FROM stocks WHERE name = ?", stock['symbol'])
        portfolio_rows = 0
        if len(stock_rows) == 1:
            portfolio_rows = db.execute("SELECT COUNT(*) FROM portfolios WHERE user_id = ? AND stock_id = ?", session["user_id"], stock_rows[0]['id'])[0]['COUNT(*)']

        if portfolio_rows == 0:

            # Firstly we check if the stock exists.
            # We add it to the database if it does not and proceed.
            stock_rows = db.execute("SELECT name FROM stocks WHERE name = ?", stock['symbol'])
            if len(stock_rows) != 1:
                db.execute("INSERT INTO stocks (name) VALUES (?)", stock['symbol'])

            # Here we are sure the stock now exists.
            stock_id = db.execute("SELECT id FROM stocks WHERE name = ?", stock['symbol'])[0]['id']
            db.execute("INSERT INTO portfolios (user_id, stock_id, shares) VALUES (?, ?, ?)", session["user_id"], stock_id, shares)

            # after these lines of code are executed, we have reduced the user's cash and (maybe) we have registered new stock in the database, and created that portfolio
        else:
            # here we know that the stock exists and the user has a portfolio with that stock, so we will just increase the shares and reduce the user's cash
            db.execute("UPDATE portfolios SET shares = shares + ? WHERE user_id = ? AND stock_id = ?", shares, session["user_id"], stock_rows[0]["id"])


    db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", transaction_sum, session["user_id"])

    return redirect("/?message=bought")

# @app.route("/sell", methods=["POST"])
# @login_required
# def sell():


@app.route("/check", methods=["POST"])
@login_required
def check():
    symbol = request.json
    if lookup(symbol) == None:
        result = False
    else:
        result = True

    return json.dumps({'isValid': result})


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        symbol = request.json
        if not symbol:
            return None
        stock = lookup(symbol)
        if not stock:
            return None

        return stock
    """Get stock quote."""
    return apology("TODO")

@app.route("/quotejson", methods=["POST"])
@login_required
def quote_json():
    symbol = request.json
    if not symbol:
            return None
    stock = lookup(symbol)
    if not stock:
        return None
    return json.dumps({"stock": stock})


@app.route("/error")
@login_required
def error(message):
    return apology(message)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        result = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(result) > 0:
            return apology("USER EXISTS")

        if not username or not password or not confirmation:
            return apology("EMPTY FIELDS DETECTED")

        if password != confirmation:
            return apology("PASSWORD MUST EQUAL CONFIRMATION")

    """Register user"""
    hash = generate_password_hash(password, 'pbkdf2', 16)

    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
    rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

    session["user_id"] = rows[0]['id']
    return redirect("/?message=registered")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
