import sqlite3

from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "12345"


# direct to home page and set method
@app.route("/", methods=["GET"])
def home():
    # check if the username is not in session
    if "username" not in session:
        # redirect them to the log in page
        return redirect("/login")
    # generate output from the index html
    return render_template("index.html")


# direct to deposit page and set methods
@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    # check if the username is not in session
    if "username" not in session:
        return redirect("/login")
    # check if the method is get
    if request.method == "GET":
        # generate output from the deposit html
        return render_template("deposit.html")
    # check if the method is post
    elif request.method == "POST":
        # validate the amount is entered
        if request.form["amount"] is None or request.form["amount"] == "":
            return render_template("deposit.html", error="Amount is required")
        # insert values into the transactions table in the database
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        sql = "INSERT INTO transactions(amount, transaction_type, username) values(?, ?, ?)"
        cursor.execute(sql, (request.form["amount"], "deposit", session["username"],))
        conn.commit()
        conn.close()
        return redirect("/")


# direct to withdraw page and set methods
@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    # check if the username is not in session
    if "username" not in session:
        return redirect("/login")
    # check if the method is get
    if request.method == "GET":
        # generate output from the withdraw html
        return render_template("withdraw.html")
    # check if the method is post
    elif request.method == "POST":
        # validate the amount is entered
        if request.form["amount"] is None or request.form["amount"] == "":
            return render_template("withdraw.html", error="Amount is required")
        # insert values into the transactions table in the database
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        sql = "INSERT INTO transactions(amount, transaction_type, username) values(?, ?, ?)"
        cursor.execute(sql, (request.form["amount"], "withdraw", session["username"],))
        conn.commit()
        conn.close()
        return redirect("/")


# direct to transactions page and set method
@app.route("/transactions", methods=["GET"])
def transactions():
    # check if the username is not in session
    if "username" not in session:
        return redirect("/login")
    # get all values from the transactions table in the database and display
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    sql = "SELECT transaction_id, amount, transaction_type FROM transactions WHERE username = ?"
    cursor.execute(sql, (session["username"],))
    results = cursor.fetchall()
    # create a transaction list
    transactions_list = []
    # loop through the results
    for row in results:
        # create transaction dictionary
        transaction = {}
        # assign transaction id in the dictionary
        transaction["transaction_id"] = row[0]
        # check what type of transaction type it is and assign the amount to the dictionary
        if row[2] == "withdraw":
            transaction["amount"] = f'-${row[1]}'
        else:
            transaction["amount"] = f'${row[1]}'
        # assign transaction type in the dictionary
        transaction["transaction_type"] = row[2]
        # append the transaction dictionary to the list
        transactions_list.append(transaction)
    conn.close()
    return render_template("transactions.html", transactions_list=transactions_list)


# direct to balance page and set method
@app.route("/balance", methods=["GET"])
def balance():
    # check if the username is not in session
    if "username" not in session:
        return redirect("/login")
    # get all values from the transactions table in the database and display
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    sql = "SELECT amount, transaction_type FROM transactions WHERE username = ?"
    cursor.execute(sql, (session["username"],))
    results = cursor.fetchall()
    # create a total variable and assign it to 0
    total = 0
    # loop through the results
    for row in results:
        # assign amount and convert to float
        amount = float(row[0])
        # create and assign transaction type variable
        transactionType = row[1]
        # check what type of transaction it is and subtract or add to the total
        if transactionType == "withdraw":
            total -= amount
        elif transactionType == "deposit":
            total += amount
    return render_template("balance.html", total=total)


# direct to login page and set methods
@app.route("/login", methods=["GET", "POST"])
#
def login():
    # check if the username is in session
    if "username" in session:
        return redirect("/")
    # check if the method is get
    if request.method == "GET":
        # generate output from the index html
        return render_template("login.html")
    # check if the method is post
    elif request.method == "POST":
        # get all values from the users table in the database
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        sql = "SELECT username FROM users WHERE username = ? AND password = ?"
        cursor.execute(sql, (request.form["username"], request.form["password"],))
        results = cursor.fetchall()
        # check if user is in the database
        if len(results) == 0:
            return render_template("login.html", error="Invalid username or password")
        else:
            # user is in the database
            session["username"] = results[0][0]
            conn.close()
            return redirect("/")


# direct to log out page and set method
@app.route("/logout", methods=["GET"])
def logout():
    # end the username session
    session.pop("username", None)
    return redirect("/login")


app.run(host="0.0.0.0")
