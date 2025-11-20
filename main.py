from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    # Optional fields
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(50))


app = Flask(__name__)

# don't forget to source data.env file before running
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
google_maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
Bootstrap5(app)

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html", google_maps_api_key=google_maps_api_key)

@app.route('/search')
def search():
    query = request.args.get("query", "")
    if query:
        cafes = Cafe.query.filter(
            Cafe.name.ilike(f"%{query}%") |
            Cafe.location.ilike(f"%{query}%")
        ).all()
    else:
        cafes = []

    return render_template("search.html", cafes=cafes, query=query)

@app.route('/service')
def service():
    return render_template('service.html')
@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(debug=True)
