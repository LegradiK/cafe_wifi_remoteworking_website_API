# ☕ London Café Finder — Flask Web App

A web application that helps users discover, save, and manage their favourite cafés across London.
Users can search by region and amenities, create accounts, upload cafés they love, and edit their previously added entries.

## 🌟 Features
### 🔍 Search Cafés

*Users can search cafés by:*

- Name

- Region (North, South, East, West, Central London)

- WiFi availability

- Power sockets

- Toilets

- Call-friendly environment

- Minimum seats

- Maximum coffee price

*Search results include:*

- Café image

- Google Maps link

- Coordinates extracted automatically from Google Maps URLs

- Amenities and seating information

### 👤 User Accounts

- Secure registration with password hashing

- Login and logout

- Sessions maintained via Flask session

### ➕ Add & Manage Your Cafés

- Logged-in users can:

- Add new cafés

- Upload an optional image

- Save Google Maps links (coordinates are auto-extracted)

- Edit previously added cafés

- View a personalised My Cafés dashboard

- Each café entry is linked to the user who created it.

### 🛠 Tech Stack

**Backend:**

- Flask

- Flask SQLAlchemy

- Werkzeug Security

- Python Dotenv

- Flask Bootstrap 5

**Database:**

- SQLite

**Frontend:**

- HTMLCodex "Koppee" Coffee Shop Template

- Bootstrap 5

- Customised Jinja templates

## 📁 Project Structure (simplified)
```bash
project/
│
├── static/
│   ├── cafe_images/
│   ├── css/
│   ├── js/
│   └── img/
│
├── templates/
│   ├── index.html
│   ├── search.html
│   ├── login_signup.html
│   ├── add_cafe.html
│   ├── edit_cafe.html
│   ├── my_cafes.html
│   └── (other template pages)
│
├── cafes.db
├── main.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation & Setup
1. Clone the repository
```bash
git clone https://github.com/LegradiK/cafe_wifi_remoteworking_website_API.git
cd cafe_wifi_remoteworking_website_API
```
2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate     # Linux
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Create environment variable file
```bash
Create a .env file:
FLASK_SECRET_KEY=your_secret_key_here
```
5. Run the application
```bash
python app.py
```

*The site will be available at:*
http://127.0.0.1:5000

## 🗺 Regions Covered

The app currently supports London regions used for filtering:

- North — Haringey, Islington, Camden, Barnet

- South — Lambeth, Southwark, Greenwich, Croydon, Peckham, Bermondsey

- East — Hackney, Tower Hamlets, Whitechapel

- West — Hammersmith, Ealing, Kensington, South Kensington

- Central — Soho, Shoreditch, Westminster, Holborn, etc.

These can be customised in REGION_MAP.

## 🧠 How the App Works (Code Summary)

- Users and cafés are stored in SQLite using SQLAlchemy models.

- Each Café has a user_id linking it to the creator.

- Google Maps URLs are parsed using a regex function to extract coordinates.

- Image uploads are stored in static/cafe_images.

- Authentication is required only for member-only pages, such as:

   - /add_cafe — Add a new café

   - /my_cafes — View user’s cafés

   - /edit_cafe/<int:cafe_id> — Edit cafés added by the user

   These routes check session['user_id'] before allowing access.

-  Public pages like /, /search, /about, /menu, /contact are accessible without login.

- Bootstrap 5 provides styling across all pages.

## 🖼 Credits
## Website Template

- Template Name: KOPPEE – Coffee Shop HTML Template

- Template Link: https://htmlcodex.com/coffee-shop-html-template

- Template Licence: https://htmlcodex.com/license

- Template Author: HTML Codex

- Author Website: https://htmlcodex.com

*About HTML Codex:*
HTML Codex is a major publisher of free and premium HTML templates, landing pages, email templates, and snippets.
Read more at: https://htmlcodex.com/about-us

## Photos

- Afta Putta Gunawan
https://www.pexels.com/photo/assorted-decors-with-brown-rack-inside-store-683039/

- Ahmet Yüksek
https://www.pexels.com/photo/cozy-winter-latte-in-graz-austria-29784884/

## 📜 Licence

**This project uses the Koppee HTML Template under the HTML Codex commercial licence.**
Ensure compliance with their licence terms when modifying or deploying the template.

Custom Flask backend code is free to use and modify as you wish.
