#  CS50 Final Project - EKSU FIVE A-SIDE
# Description:
Web App to keep tracks of football activities and players,the front consist of CSS and HTML while the backend consist of python and flask framework, and also an sqlite3 database to store all the users data, and JIMJA templates is used to duplicate and seperate the layouts on each html pages. The webapp is for football players, keep record of all the players and matches created, matches joined by each players or users.
the project ~/project consist of three folders and two python script and one sqlite databse and one requirement text file.
Technology used are:
-Python
-SQlite3
-FLASK
-Images
-JINJA templates
## How the webopage works?
When the webpage is first opened with get the user is directed to sigin or register, if the user choose to register as a first timer we will be ask for the following information
-Pick a unique usersname
-Choose a paasword which in turn is hashed and then stored
-Email
-Phone Number
-Checkbox favored feet
-Checkbox Position
-Checkbox Physique Details

if the users registration was sucessfully, he will redirect to login page to login and he can access the nav-bar in full and can veiw his profile details and change the default profile picture to his preferred choiced. on the home page is the matches crteated by the user in the web app, the user can choose to the following.
-create match
-join match which has been created by other users
-delete and edit the match he created himself but not for others.
-users can only delete or edit matchcreated by oneself
-user can also choose to change password
-user can also choose to delete profile
the create natch page gives user the chance to create his own match with details like hostname, time,date and number of players needed, after creating the match it will be added to list match in home page.
if user is not logged in, he can only see the list of match he can neither join or create match, becausesome options wont be access until you log in.
users can choose chose to join match, by clicking on the join match button, and their information will be displayed in a table with other users who have joined before them.
### Routing
the routes are either by get or post which checked by app.route functions, and some requires the users to be logged in before the route can be accessed.
### Session
with the help of the flask_session library, the webpage is able is able to confirm if the user is registered, once the user logins the session is stored. all the user info can be accessed with request from end end to backend through flask server.
### Static FILes;
path/project/static/style.css and also the (./project/static/images) file which contain the profile pictures which the user of have upload.
## Python Script;
project/app.py: the script contains the route for all the rendering the templates and as well as the flask functions. the script also helps withe the function thats allow to convert and stored images has strings in the database.
```python
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
```
project/help.py:  the script help with the session which the user logged into and cookies to help. also with the request and URL

## Database;
./project/fiveaside.db : this datable consist of two table which are named players and matchs, the players table keeps records of all players info. and contains all the info
of matches created.

The Frontend consist of css and html and jinja to render the templates
The Backend consist of python and flask framework

## Requirement;
project/requirements.txt consist of all the flask and python extensions libraries like cs50 and flask_session

## Possible Improvements?
*create friends list
*User be able to add each has friends
*chat with each other
*home page to display all users pictures and little descpriptions
*Hide the edit and delete from user who didnt create such match
*Create form classes that are reausable.

## Documentation
https://flask.palletsprojects.com/en/2.1.x/

https://flask-sqlalchemy.palletsprojects.com/en/2.x/

https://flask-wtf.readthedocs.io/en/stable/form.html#module-flask_wtf.file

## About CS50
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

Thank you for all CS50.
#### Video Demo:  <https://youtu.be/-DpP_lPnw_E>