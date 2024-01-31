
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "12345"

# direct to home page and set method
@app.route("/", methods = ["GET"])
# home page
def home():
    # check if the username is not in session
    if "username" not in session:
        # redirect them to the log in page
        return redirect("/login")
    # generate output from the index html
    return render_template("index.html")

# direct to deposit page and set methods
@app.route("/deposit", methods = ["GET", "POST"])
# deposit page
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
        # establish connection with the data base
        conn = sqlite3.connect("data.db")
        # create the data base cursor
        cursor = conn.cursor()
        # insert values into the rows of the transactions table
        sql = "INSERT INTO transactions(amount, transaction_type, username) values(?, ?, ?)"
        #
        cursor.execute(sql, (request.form["amount"], "deposit", session["username"], ))
        #
        conn.commit()
        # close the data base
        conn.close()
        return redirect("/")

# direct to withdraw page and set methods
@app.route("/withdraw", methods = ["GET", "POST"])
#
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
        #
        conn = sqlite3.connect("data.db")
        #
        cursor = conn.cursor()
        #
        sql = "INSERT INTO transactions(amount, transaction_type, username) values(?, ?, ?)"
        #
        cursor.execute(sql, (request.form["amount"], "withdraw", session["username"], ))
        #
        conn.commit()
        #
        conn.close()
        return redirect("/")

# direct to transactions page and set method
@app.route("/transactions", methods = ["GET"])
def transactions():
    # check if the username is not in session
    if "username" not in session:
        return redirect("/login")
    #
    conn = sqlite3.connect("data.db")
    #
    cursor = conn.cursor()
    #
    sql = "SELECT transaction_id, amount, transaction_type FROM transactions WHERE username = ?"
    #
    cursor.execute(sql, (session["username"], ))
    #
    results = cursor.fetchall()
    #
    transactions_list = []
    #
    for row in results:
        transaction = {}
        transaction["transaction_id"] = row[0]
        if row[2] == "withdraw":
            transaction["amount"] = f'-${row[1]}'
        else:
            transaction["amount"] = f'${row[1]}'


        transaction["transaction_type"] = row[2]
        transactions_list.append(transaction)
    conn.close()
    return render_template("transactions.html", transactions_list = transactions_list)

# direct to balance page and set method
@app.route("/balance", methods = ["GET"])
def balance():
    # check if the username is not in session
    if "username" not in session:
        return redirect("/login")
    #
    conn = sqlite3.connect("data.db")
    #
    cursor = conn.cursor()
    #
    sql = "SELECT amount, transaction_type FROM transactions WHERE username = ?"
    #
    cursor.execute(sql, (session["username"], ))
    #
    results = cursor.fetchall()
    #
    total = 0
    #
    for row in results:
        amount = float(row[0])
        transactionType = row[1]
        if transactionType == "withdraw":
            total -= amount
        elif transactionType == "deposit":
            total += amount
    return render_template("balance.html", total = total)

# direct to login page and set methods
@app.route("/login", methods = ["GET", "POST"])
#
def login():
    # check if the username is in session
    if "username" in session:
        return redirect("/")
    #
    if request.method == "GET":
        #
        return render_template("login.html")
    #
    elif request.method == "POST":
        #
        conn = sqlite3.connect("data.db")
        #
        cursor = conn.cursor()
        #
        sql = "SELECT username FROM users WHERE username = ? AND password = ?"
        #
        cursor.execute(sql,(request.form["username"], request.form["password"],))
        #
        results = cursor.fetchall()
        #
        if len(results) == 0:
            #
            return render_template("login.html", error = "Invalid username or password")
        else:
            #
            session["username"] = results[0][0]
            #
            conn.close()
            return redirect("/")

# direct to log out page and set method
@app.route("/logout", methods = ["GET"])
#
def logout():
    #
    session.pop("username", None)
    return redirect("/login")


app.run(host="0.0.0.0")