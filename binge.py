# import necessary libraries
import json
from bson import json_util, ObjectId
from flask import Flask, render_template, jsonify, redirect, url_for, request, session, Response
from flask_pymongo import PyMongo
import requests
import json

# from flask_bcrypt import bcrypt
# from flask.ext.pymongo import PyMongo

from config import tmdb_api, omdb_api, MONGO_URI  ## tmdb API Key = tmdb_api  ## omdb API key = omdb_api

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config['MONGODB_NAME'] = bingeworthy_db
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send_form1", methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        users = mongo.db.users

        # note: email == username as well as email
        # store all the form values as variables
        email = request.form['email']
        password = request.form['password']

        # check for login first. There are many combinations, but 
        # for now let's just test if we have a simple login name 
        # and password
        if email and password:
            existing_user = users.find_one({'email': email})
            if existing_user:
                if password == existing_user['pwd']:
                    return redirect('/shows')
                else:
                    return "Invalid username or password"
            else:
                return "That username is not registered"
        else:
            return "Invalid password / Username combination"
    else:
        return redirect("/")


@app.route("/send_form2", methods=['POST', 'GET'])
def send_form2():
    if request.method == 'POST':
        users = mongo.db.users
        new_email = request.form['new_email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        screen_name = request.form['screen_name']
        group = request.form['group']
        genre = request.form['genre']
        gender = request.form['gender']

        # first step make sure all the fields are filled in
        if new_email and password1 and password2:
            existing_user = users.find_one({'email': new_email})

            # if this the username/email is take then stop
            if existing_user:
                return "That username already exists"

            # if the username is not in use
            else:
                # verify that both passwords match
                if password1 == password2:
                    # storing the bcrypt method below for future. bcrypt is not working.
                    # password = bcrypt.hashpw(request.form['password1'].encode('utf-8') , bcrypt.gensalt()) #bcrypt not working
                    password = password1
                    users.insert({'email': new_email, 'pwd': password, 'first_name': first_name, \
                                  "last_name": last_name, 'screen_name': screen_name, 'groups': group, \
                                  'genres': genre, 'gender': gender})
                    return redirect('/shows')
                else:
                    return "Passwords don't match"
        else:
            return "Please fill in all the fields"
    else:
        return redirect("/")


@app.route("/shows")
def shows():
    return render_template("shows.html")


@app.route("/shows/data")
def shows_data():
    shows = mongo.db.shows_omdb.find()
    print(shows)
    shows = json.loads(json_util.dumps(shows))
    return jsonify(shows)

# Note: I am commenting the function because it lint was returning
# errors.  I put the same in the def show_add below

# def omdb_search(title, show_type, year):
#     omdb_url = "http://www.omdbapi.com/?i=tt3896198&apikey=" + omdb_api
#     title = title.split(' ')
#     title='+'.join(title)
#     title = '&s=' + title
#     show_type = '&type=' + show_type
#     year = '&y=' + year
    
#     omdb_url = omdb_url + title + show_type + year
#     omdb_data = requests.get(omdb_url)
#     omdb_url = omdb_data.url
#     omdb_data=omdb_data.json()
#     return(omdb_data)

@app.route("/show_add", methods=['POST','GET'])
def show_add():
    if request.method == 'POST':
        title = request.form['title']
        show_type = request.form['show_type']
        year = request.form['year']
        # specific/general refer to checkbox for title search or general search
        # the title search has more detailed information 
        # we will use title searches to populate MongoDB
        # specific = request.form['specific']
        # general = request.form['general']

        if title == False:
            return "You need to enter a title"
        else:
            omdb_url = "http://www.omdbapi.com/?i=tt3896198&apikey=" + omdb_api
            title = title.split(' ')
            title='+'.join(title)
            # using &t is a title search which returns 1 result
            title = '&t=' + title
            show_type = '&type=' + show_type
            year = '&y=' + year
            
            omdb_url = omdb_url + title + show_type + year
            omdb_data = requests.get(omdb_url)
            omdb_url = omdb_data.url
            omdb_data=omdb_data.json()
            return
    else:
        pass


@app.route("/users/data")
def users_data():
    users = mongo.db.users.find()
    print(users)
    users = json.loads(json_util.dumps(users))
    return jsonify(users)


# This uses secret key to connect
# if __name___ == "__main__":
#     app.secret_key = "mysecret"
#     app.run(debug=true)

# the is the standard flask connection
if __name__ == "__main__":
    app.run(debug=True)
