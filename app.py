import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'super secret key'
Session(app)

db = SQL("sqlite:///userAccounts.db")


# Route for handling the login page logic
@app.route('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get("register"):
            return render_template("register.html")
        username = request.form.get("username")
        password = request.form.get("password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or password != rows[0]['password']:
            error = 'Invalid Credentials. Please try again.'
            #return render_template('register.html')
        else:
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            return render_template('homepage.html')
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("Wrong password", 400)

        # Ensure confirmation and password are the same
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)
        
        # Ensure the username is not in the database already
        usernameDatabase = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # If username in database then apology
        if len(usernameDatabase) != 0:
            return apology("Username is already in use, pick another one", 400)
        
        # Add username and password to database
        userid = db.execute("INSERT INTO users (username, password) VALUES (?, ? )", 
                request.form.get("username"), request.form.get("password"))

        # Assigning the userid to the session
        session["user_id"] = userid

        return render_template("homepage.html")

    else:
        return render_template("register.html")

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code