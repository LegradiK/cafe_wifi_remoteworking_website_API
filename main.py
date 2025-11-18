from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
import pandas as pd
import os

app = Flask(__name__)

# don't forget to source data.env file before running
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
google_maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
Bootstrap5(app)

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html", google_maps_api_key=google_maps_api_key)

@app.route("/search")
def search():
    return render_template("listing.html", google_maps_api_key=google_maps_api_key)

@app.route("/explore")
def explore():
    return render_template("listing.html", google_maps_api_key=google_maps_api_key)

@app.route("/listing")
def listing():
    return render_template("listing.html", google_maps_api_key=google_maps_api_key)

@app.route("/add_listing")
def add_listing():
    return render_template("listing.html", google_maps_api_key=google_maps_api_key)

@app.route("/single_listing")
def single_listing():
    return render_template("single_listing.html", google_maps_api_key=google_maps_api_key)

@app.route("/contact")
def contact():
    return render_template("contact.html", google_maps_api_key=google_maps_api_key)

@app.route("/auth_login")
def auth_login():
    return render_template("auth_login.html", google_maps_api_key=google_maps_api_key)


if __name__ == '__main__':
    app.run(debug=True)
