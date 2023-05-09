import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from help import login_required
import uuid as uuid



UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure folder to use filesystems
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///fiveaside.db")

# Create a new table and index to keep track of the of users transactions

#if not os.environ.get("API_KEY"):
    #raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure the user input a valid username
        if not request.form.get("username"):
            flash('must input username')
        # Ensure the password is coreect
        elif not request.form.get("password"):
             flash('must input password')
        # Query the database for valid username
        rows = db.execute("SELECT *FROM players where username =?", request.form.get("username"))

        # Query the databse for correct password
        if len(rows) != 1 or not check_password_hash(rows[0]['hash'], request.form.get("password")):
            flash('inavlid username and/or password')

        # Remeber which user has logged in
        session["player_id"] = rows[0]["id"]

        # Redirect user to profile
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/home")
def home():
    # Get all the matches avaliable info

    match = db.execute("SELECT name, date, location, time, number_of_players FROM matchs")

    playerid = (db.execute("SELECT player_id FROM matchs")[0]["player_id"])
    if playerid:
        return render_template("home.html", match=match, playerid=playerid)
    return render_template("home.html", match=match)


@app.route("/playersi", methods=["GET", "POST"])
def playersi():

    # Validate users input
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    email = request.form.get("email")
    position = request.form.get("position")
    gender = request.form.get("gender")
    body = request.form.get("body")
    favored = request.form.get("favored")
    height = request.form.get("height")
    phone = request.form.get("phone")
    error = None
    users = db.execute("SELECT username FROM players WHERE username =?", username)


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure the username, password, confirmation password and all was submitted
        if not username or not password or not confirmation or not email or not position or not body or not height or not favored or not gender or not phone:
            error = 'all form must be filled'
        # Ensure that the password is same iwth confirm password
        if password != confirmation:
            error = 'password must match'
        # Ensure the username does not exist before
        if users:
            error = 'username already taken'
        # Proceed to convert the password amd register the new user
        else:
            # Hash the password
            hash = generate_password_hash(password)

            # Insert the new user information into the databse
            db.execute("INSERT INTO players (username, hash, position, email, name, gender, body_build, favored_feet, height, phone) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", username, hash, position, email, name, gender, body, favored, height, phone)

            session["player_id"] = ["id"]

            # Redirect user back to homepage
            flash("you've being successfully registered!")
            return redirect("/login")

    # User reach the page via GET method
    return render_template("playersi.html", error=error)


@app.route("/playersprofile")
def playersprofile():

    # Obtain all the information needed from the players database
    playersprofile = db.execute("SELECT *FROM players WHERE id = ?", session["player_id"])

    # Selecting the info needed to render in the template
    return render_template("playersprofile.html", playersprofile=playersprofile)

@app.route("/delete", methods=["GET", "POST"])
def delete():

    if request.method == "POST":
        # Select profile to be deleted from the database

        # Validate users input
        if request.form["no"] == 'no':
            return redirect("/playersprofile")


            # Select profile to be deleted from the database
            # # Redirect back to login page
        elif request.form["yes"] == 'yes':
            db.execute("DELETE FROM players where id =?", session["player_id"])
            flash("your profile has been deleted succesfully")
            return redirect("/login")

    else:
        return render_template("delete.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():

    if request.method == "POST":
    # Select the needed value from the database to be edited
        db.execute("SELECT *FROM players WHERE id = ?", session["player_id"])
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        position = request.form.get("position")
        gender = request.form.get("gender")
        body = request.form.get("body")
        favored = request.form.get("favored")
        height = request.form.get("height")
        phone = request.form.get("phone")


        db.execute("UPDATE players SET name = ?, username = ?, email = ?, position = ?, gender = ?, body_build = ?, favored_feet = ?, height = ?, phone = ? WHERE id = ?",
                    name, username, email, position, gender, body, favored, height, phone, session["player_id"])
        return redirect("/playersprofile")
    else:
        return render_template("edit.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'picture' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['picture']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            picn = str(uuid.uuid1()) + "_" + filename
            saver = request.files['picture']
            file = picn
            db.execute("UPDATE players SET picture = ? WHERE id =?", picn , session["player_id"])
            saver.save(os.path.join(app.config['UPLOAD_FOLDER'], picn))
            return redirect("/playersprofile", picn)

    return render_template("upload.html")



@app.route("/match", methods=["GET", "POST"])
def match():
    # Get all the form input
    creator = request.form.get("matchcc")
    timedd = request.form.get("timee")
    number = request.form.get("pee")
    locale = request.form.get("lee")
    datedd = request.form.get("datee")

    # Method of route for post
    if request.method == "POST":
        # Validate all the forms
        if not creator or not timedd or not locale or not number or not datedd:
            flash("all form must be filled")
        else:
            db.execute("INSERT INTO matchs (player_id, name, location, time, date, number_of_players) VALUES(?, ?, ?, ?, ?, ?)", session["player_id"], creator, locale, timedd, datedd, number)
            flash("you've created a match successfully")
            return redirect ("/home")

    return render_template("match.html")



@app.route("/home/editmatch/<int:id>", methods=["GET", "POST"])
@login_required
def editmatch(id):
    # Method of route is post
    if request.method == "POST":
        #Select all the needed information
        (db.execute("SELECT *FROM matchs WHERE player_id =?", session["player_id"]))

        if session["player_id"]:
            # Get all the needed form
            # Select all the needed information
            creatorr = request.form.get("matchc")
            tim = request.form.get("timeo")
            numb = request.form.get("peui")
            loca = request.form.get("leo")
            datei = request.form.get("dateo")

            # Method of route is post

            # Update match details
            db.execute("UPDATE matchs SET name = ?, time = ?, number_of_players = ?, location = ?, date = ? WHERE player_id = ?",
                        creatorr, tim, numb, loca, datei, session["player_id"])
            flash("match details updated sucessfully")
            return redirect("/home")
        else:
            flash("your not authorized to edit this post")
            return render_template("home.html")
    return render_template("editmatch.html")



@app.route("/home/deletematch>", methods=["GET","POST"])
def deletematch():
    # Method of reqeuest is post
    if request.method == "POST":
        playerid = (db.execute("SELECT player_id FROM matchs")[0]["player_id"])
        # Choice of the user either YES or NO
        if playerid and session["player_id"]:
            if request.form["action"] == 'no':
                # User click on NO button
                flash("match was not deleted")
                return redirect("/home")
            # User click on Yes
            elif request.form["action"] == 'yes':
                matchid = (db.execute("SELECT matchs.id FROM matchs")[0]["id"])
                db.execute("DELETE FROM matchs WHERE id =?", matchid)
                flash("matched deleted successfully")
                return redirect("/home")
        else:
            flash("your not authorised to delete this match")
            return redirect("/home")
    return render_template("deletematch.html")



@app.route("/jmatch")
@login_required
def jmatch():

        #matchid = int(db.execute("SELECT matchs.id FROM matchs")[0]["id"])
        #num = int((db.execute("SELECT number_of_player FROM matchs WHERE matchs.id =?", matchid)[0]["number_of_players"]))
        #total = db.execute("SELECT COUNT *FROM matchs")
        host = db.execute("SELECT name FROM matchs")
        #if num > (total - 1):
            #flash("sorry can't join!, number of players exceeded!")
        try:
            join = db.execute("SELECT username, name, position, favored_feet, phone FROM players")
            return render_template("jmatch.html", join=join, host=host)
        except (KeyError, TypeError, ValueError):
            flash("sorry something came up")



@app.route("/home/joinmatch", methods = ["GET", "POST"])
@login_required
def joinmatch():
    #names = (db.execute("SELECT name FROM players WHERE id =? " ,session["player_id"]) )
    #position = (db.execute("SELECT position FROM players")[0]["position"])
    #feet = (db.execute("SELECT favored_feet FROM players")[0]["favored_feet"])
    #phone = (db.execute("SELECT phone FROM players")[0]["phone"])
    #matchid = (db.execute("SELECT matchs.id from matchs")[0]["id"])
    if request.method == "POST":
        if request.form["action"] == 'yes':
            #if names > 1:
                flash("you've already joined match")
                return redirect("/jmatch")
        elif request.form["action"] == 'no':
            flash("you didnt join the match")
            return redirect("/home")

    return render_template("joinmatch.html")



@app.route("/changep", methods=["GET", "POST"])
@login_required
def changep():
    passwordd = request.form.get("password")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":
        old_password = db.execute("SELECT hash FROM users WHERE id =?", session["player_id"])
        if (old_password != passwordd) or (password != confirmation):
            flash("password not matching")
        else:
            hash = generate_password_hash(password)
            db.execute("UPDATE users SET hash =? WHERE id=?", hash, session["player_id"])
            flash("password changed successfully!")
            return redirect("/home")
    return render_template("changep.html")


@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS