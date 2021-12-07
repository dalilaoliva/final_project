import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import date, datetime

today = date.today()

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'super secret key'
Session(app)

db = SQL("sqlite:///userAccounts.db")


# Route for handling the login page logic
@app.route('/')

@app.route('/login', methods=['GET', 'POST'])
def login():

    session.clear()

    if request.method == 'POST':
        if request.form.get("register"):
            return render_template("register.html")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"): 
            return apology("must provide password", 403)

        username = request.form.get("username")
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or password != rows[0]['password']:
            return apology("invalid username and/or password", 403)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return render_template('greet.html')

    else:
        return render_template('login.html')

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

        return render_template("quiz.html")

    else:
        return render_template("register.html")

# Function from finance but I changed the error image
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        # https://github.com/jacebrowning/memegen#special-characters
        #https://api.memegen.link/images/doge/~hspecial_characters~q/underscore__-dash--.png

        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


# Displays the weights that the person has done, for progress 
@app.route("/weight-log")
def weightLog():
    logs= db.execute("SELECT exercise, weight, date FROM weightLog WHERE userId=?", session['user_id'])
    
    return render_template ("weight-log.html", logs=logs)

# Sorting which workout method the user will be assigned beased on their answers to the quiz
@app.route("/quiz", methods=['GET', 'POST'])
def sorting():
    if request.method == "POST":
        number=0
        if request.form["option1"] == "home":
            if request.form["option2"] == "weightloss":
                number=1
            elif request.form["option2"] == "buildmuscle":
                number=2
            elif request.form["option2"] == "resistance":
                number=3
        if request.form["option1"] == "gym":
            if request.form["option2"] == "weightloss":
                number=4
            elif request.form["option2"] == "buildmuscle":
                number=5
            elif request.form["option2"] == "resistance":
                number=6
        db.execute("UPDATE users SET workout_style = ? WHERE id= ?", number, session['user_id'])
        return render_template("home.html", number=number)
    return render_template("quiz.html")

# Displaying a page with tutorials on the exercises depending on the setting the person has chosen in the quiz.
@app.route("/tutorials2")
def sorting2():
    workout_style = db.execute("SELECT workout_style FROM users WHERE id = ?", session['user_id'])
    wstyle=workout_style[0]['workout_style']

    if wstyle == 1 or wstyle == 2 or wstyle == 3:
        homeup = db.execute("SELECT name, link FROM videos WHERE exercise_type = 'homeup' ")
        homelow = db.execute("SELECT name, link FROM videos WHERE exercise_type = 'homelow' ")
        return render_template("tutorials2.html", homeup = homeup, homelow = homelow, wstyle = wstyle)

    elif wstyle == 4 or wstyle == 5 or wstyle == 6:
        gymup = db.execute("SELECT name, link FROM videos WHERE exercise_type = 'gymup' ")
        gymlow = db.execute("SELECT name, link FROM videos WHERE exercise_type = 'gymlow' ")
        return render_template("tutorials2.html", gymup = gymup, gymlow = gymlow, wstyle = wstyle)

    else:
        return render_template("tutorials2.html")

# Displays the workout plans for the user and the user can record the weights if used in the workout plans. 
@app.route("/home", methods=["GET", "POST"])
def workout_page():
    style = db.execute("SELECT workout_style FROM users WHERE id = ?", session['user_id'])
    number = style[0]["workout_style"]

    if request.method =="POST":

        if request.form.get("record"):

            if not request.form.get("weight") or not request.form.get("exercise"):
                return apology("Must provide the details", 403)

            db.execute("INSERT INTO weightLog (userId,exercise, weight,date) VALUES (?,?,?,?)", session['user_id'],request.form.get("exercise"), request.form.get("weight"), today)
    return render_template("home.html", number=number)

# Displays a calendar, lets record meetings or important dates for the user and displays them accoring to the month and year.  
@app.route("/calendar", methods=["GET", "POST"])
def calendar():

    if request.method =="POST":

        if request.form.get("record"):

            if not request.form.get("event") or not request.form.get("day") or not request.form.get("month") or not request.form.get("year"):
                return apology("Must provide the details", 403)

            db.execute("INSERT INTO calendar (userId, event, day, month, year) VALUES (?,?,?,?,?)", session['user_id'],request.form.get("event"), request.form.get("day"),request.form.get("month"), request.form.get("year"))
            
    user = db.execute("SELECT event, day, month, year FROM calendar WHERE userid =?", session['user_id'])
    month = datetime.now().month
    year = datetime.now().year
        
    return render_template("calendar.html", user=user, month=month, year=year)


@app.route("/greet")
def greet():
    return render_template("greet.html")