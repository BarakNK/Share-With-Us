from flask import Flask, jsonify, request, render_template, redirect, url_for
import random
from DB import *
from hashlib import sha256

def hash(password):
    salt, pepper = 'light','ning'
    password = salt + password + pepper
    return sha256(password.encode()).hexdigest()

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)
app.config['SECERET_KEY'] = 'super-seceret-key'
app.secret_key = "MY_SUPER_SECRET_KEY"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        Username = request.form['username']
        Password = request.form['password']
        if existed_user(Username, hash(Password)):
            global user_id
            user_id = query_id_by_username(Username)
            return render_template('home.html', messages = query_all_messages())

        else:
            return render_template('login.html', msg="Wrong password or username. Try again")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        Name = request.form['name']
        Username = request.form['username']
        Password = request.form['password']
        Email = request.form['email']
        if not username_exists(Username):
            add_user(Name, Username, hash(Password), Email)
            global user_id
            user_id = query_id_by_username(Username)
            return render_template('home.html', messages = query_all_messages())

        else:
            return render_template('signup.html', msg="The Username is already taken. Try another username")


@app.route('/home')
def home():
    return render_template('home.html', messages = query_all_messages())


@app.route('/share', methods=['GET', 'POST'])
def share():
    if request.method == 'POST':
        Headline = request.form['headline']
        Content = request.form['content']
        Option = request.form['option']
        Publisher_name = ''

        if Option == "Anonymously":
            Publisher_name = 'Anonymous'
        
        else:
            Publisher_name = query_by_id(user_id).username
        
        try:
            if not user_id or user_id<=0:
                return render_template('login.html', msg="In orded to share you need to log in (if you don't have a user then sign in)")

            if Headline == '' or Content == '' or Option == '':
                return render_template('share.html', msg="You cannot leave an empty segment...")

            elif message_exists(Headline, user_id):
                return render_template('share.html', msg="Seems like you have already posted the same exact messgae.")
            
            else:
                add_message(Headline, Content, Publisher_name, user_id)
                return render_template('home.html', messages = query_all_messages())
        
        except NameError:
            return render_template('login.html', msg="In orded to share you need to log in (if you don't have a user then sign in)")

        except:
            return render_template('login.html', msg="Please log in before sharing (if you don't have a user then sign in)")
    
    else:
        try:
            if user_id:
                return render_template('share.html')
            else:
                return render_template('login.html', msg="In orded to share you need to log in (if you don't have a user then sign in)")
        
        except NameError:
            return render_template('login.html', msg="In orded to share you need to log in (if you don't have a user then sign in)")
        
        except:
            return render_template('login.html', msg="Please log in before sharing (if you don't have a user then sign in)")


if __name__ == "__main__":  # Makes sure this is the main process
    app.run(  # Starts the site
        host=
        '0.0.0.0',  # EStablishes the host, required for repl to detect the site
        port=random.randint(
            2000, 9000),  # Randomly select the port the machine hosts on.
        debug=True)
