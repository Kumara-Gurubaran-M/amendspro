from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

names = ["Jin", "Kazuya", "Jun", "Azuka"]

app.config["SECRET_KEY"] = "bjdhfgyugfhasdgfusdagfjhsdgvc"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

class User(db.model):
  id = db.column(db.Integer, primary_key = True)
  username = db.column(db.String(20), nullable = False, unique = True)
  email = db.column(db.String(20), nullable = False, unique = True)
  password = db.column(db.String(120), nullable = False)
  pfp = db.column(db.String(20), nullable = False, default = "default.jpg")

  def __repr__(self): # This function specifies how the table values should be printed when data is queryed
    return f"User('{self.username}', '{self.email}', '{self.image_file}')"

@app.route("/")
def home():
  return render_template("index.html", names=names)

@app.route("/login", methods=["POST", "GET"])
def login():
  form = RegistrationForm()
  if form.validate_on_submit(): # Checking if the credentials are correct based on the RegistrationForm() method
    # Inserting values into the User Table
    user = User(username = form.username.data, email = form.email.data) 
    db.session.add(user)
    db.session.commit()
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('home'))
  return render_template("login.html", title="About", form=form)

