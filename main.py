import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'cafes.db')}"
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key')
db = SQLAlchemy(app)
Bootstrap5(app)


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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashed password

    def __repr__(self):
        return f"<User {self.email}>"

with app.app_context():
    db.create_all()
    # Sample data
    if not User.query.first():
        db.session.add(User(name="Alice Johnson", email="alice@example.com", password=generate_password_hash("password123")))
        db.session.add(User(name="Bob Smith", email="bob@example.com", password=generate_password_hash("mypassword")))
        db.session.commit()

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    cafes = []
    selected_region = request.form.get("region")

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

    # Extract coordinates from map_url
    cafes_data = []
    for cafe in cafes:
        try:
            coords_part = cafe.map_url.split("/@")[1].split(",")
            lat = float(coords_part[0])
            lng = float(coords_part[1])
            cafes_data.append({
                "id": cafe.id,
                "name": cafe.name,
                "location": cafe.location,
                "img_url": cafe.img_url,
                "lat": lat,
                "lng": lng,
                "seats": cafe.seats,
                "coffee_price": cafe.coffee_price,
                "has_wifi": cafe.has_wifi,
                "has_sockets": cafe.has_sockets,
                "has_toilet": cafe.has_toilet,
                "can_take_calls": cafe.can_take_calls,
                "map_url": cafe.map_url
            })
        except Exception as e:
            # Skip cafes with invalid URLs
            continue

    return render_template(
        "search.html",
        cafes=cafes_data
    )

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Login successful
            session['user_name'] = user.name
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            # Login failed
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login_signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('signup'))

        # Optional: check if user already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('login_signup.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route("/add-cafe", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        address = request.form.get("address")
        map_url = request.form.get("map_url")
        seats = request.form.get("seats")
        coffee_price = request.form.get("coffee_price")
        has_sockets = bool(request.form.get("has_sockets"))
        has_toilet = bool(request.form.get("has_toilet"))
        can_take_calls = bool(request.form.get("can_take_calls"))

        # Image upload
        file = request.files.get("img_url")
        if file:
            img_path = os.path.join("static/cafe_images", file.filename)
            file.save(img_path)
            img_url = img_path
        else:
            img_url = ""

        new_cafe = Cafe(
            name=name,
            location=location,
            map_url=map_url,
            img_url=img_url,
            seats=seats,
            coffee_price=coffee_price,
            has_sockets=has_sockets,
            has_toilet=has_toilet,
            can_take_calls=can_take_calls
        )

        db.session.add(new_cafe)
        db.session.commit()
        flash("Cafe added successfully!", "success")
        return redirect(url_for("search"))

    return render_template("add_cafe.html")


if __name__ == '__main__':
    app.run(debug=True)
