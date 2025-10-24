from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, IntegerField, DateField
from wtforms.validators import DataRequired, URL, Optional
import pandas as pd
import os

app = Flask(__name__)

# don't forget to source data.env file before running
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
Bootstrap5(app)


class CafeWifiForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ratings = IntegerField('Ratings (0 - 100points)', validators=[DataRequired()])
    comfort = SelectField('Comfort', choices=[('☠️', '☠️'), ('☠️☠️', '☠️☠️'), ('☠️☠️☠️', '☠️☠️☠️'), ('☠️☠️☠️☠️', '☠️☠️☠️☠️'), ('☠️☠️☠️☠️☠️', '☠️☠️☠️☠️☠️')], validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    google_map = StringField('Google map link', validators=[DataRequired(),URL(require_tld=True, message='googlemap location link required')])
    hike_distance = FloatField('Hike Distance (in km)', validators=[DataRequired()])
    hike_time = IntegerField('Estimated Time (in min)', validators=[DataRequired()])
    home_distance = FloatField('Distance from Home (in km)', validators=[DataRequired()])
    parking = SelectField('Parking Available', choices=[('🅿️👍','🅿️👍'),('🅿️💸','🅿️💸'),('🚫','🚫')])
    toilet = SelectField('Toilet Available', choices=[('🚽','🚽'),('💩','💩')])
    date_visited = SelectField(
        'Visited?',
        choices=[
            ('Yes', 'Yes - Specify Date below'),
            ('Yes - No date', 'Yes - No date'),
            ('Not Yet', 'Not Yet')
        ],
        default='known'
    )
    date = DateField('Date', format='%Y-%m-%d', validators=[Optional()])

    submit = SubmitField('Submit')

CSV_FORM = 'hiking-data.csv'

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = HikingForm()
    if form.validate_on_submit():
        if form.date_visited.data == "Yes":
            hike_date = form.date.data
        else:
            hike_date = "🙅🏻"

        new_data = {
            'Name': form.name.data,
            'Ratings': form.ratings.data,
            'Difficulty': form.difficulty.data,
            'Location': form.location.data,
            'Google map link': form.google_map.data,
            'Hike Distance (in km)': form.hike_distance.data,
            'Estimated Time (in min)': form.hike_time.data,
            'Distance from Home (in km)': form.home_distance.data,
            'Parking Available': form.parking.data,
            'Toilets Available': form.toilet.data,
            'Visited?': form.date_visited.data,
            'Date': hike_date
        }

        dataframe = pd.read_csv(CSV_FORM)
        new_data_df = pd.DataFrame([new_data])
        # Append new data to the DataFrame
        dataframe = pd.concat([dataframe, new_data_df], ignore_index=True)
        # Save the updated DataFrame back to the CSV
        dataframe.to_csv(CSV_FORM, index=False)
        print("Updated")
        return redirect(url_for('hikes'))

    return render_template('add.html', form=form)


@app.route('/hikes')
def hikes():
    datafile = pd.read_csv(CSV_FORM)
    data = datafile.to_dict(orient='records')
    return render_template('hiking_places.html', hills=data)


if __name__ == '__main__':
    app.run(debug=True)
