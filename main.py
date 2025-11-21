from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'cafes.db')}"
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
db = SQLAlchemy(app)
Bootstrap5(app)
google_maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY")

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

REGION_MAP = {
    "north": ["Haringey", "Islington", "Camden", "Barnet"],
    "south": ["Lambeth", "Southwark", "Greenwich", "Croydon", "Peckham", "Bermondsey"],
    "east": ["Hackney", "Tower Hamlets", "Whitechapel"],
    "west": ["Hammersmith", "Ealing", "Kensington", "South Kensington"],
    "central": ["Westminster", "Camden Town", "Holborn", "Soho", "Shoreditch", "Clerkenwell", "Borough", "London Bridge", "Bankside", "Barbican"]
}

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html", google_maps_api_key=google_maps_api_key)

@app.route("/search", methods=["GET", "POST"])
def search():
    cafes = []
    selected_region = request.form.get("region")
    view_type = request.args.get("view_type", "grid")

    query = Cafe.query

    if request.method == "POST":
        name = request.form.get("name")
        has_wifi = request.form.get("has_wifi")
        has_sockets = request.form.get("has_sockets")
        has_toilet = request.form.get("has_toilet")
        can_take_calls = request.form.get("can_take_calls")
        min_seats = request.form.get("min_seats")
        max_price = request.form.get("max_price")

        if name:
            query = query.filter(Cafe.name.ilike(f"%{name}%"))

        if selected_region and selected_region in REGION_MAP:
            query = query.filter(Cafe.location.in_(REGION_MAP[selected_region]))

        if has_wifi:
            query = query.filter_by(has_wifi=True)
        if has_sockets:
            query = query.filter_by(has_sockets=True)
        if has_toilet:
            query = query.filter_by(has_toilet=True)
        if can_take_calls:
            query = query.filter_by(can_take_calls=True)
        if min_seats:
            query = query.filter(Cafe.seats.cast(db.Integer) >= int(min_seats))
        if max_price:
            query = query.filter(Cafe.coffee_price.cast(db.Float) <= float(max_price))

        cafes = query.all()
    return render_template("search.html", cafes=cafes, view_type=view_type)

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
