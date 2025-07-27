from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ParkingLotForm(FlaskForm):
    prime_location_name = StringField("Location Name", validators=[DataRequired()])
    price_per_hour = FloatField("Price per Hour (₹)", validators=[DataRequired(), NumberRange(min=0)])
    address = StringField("Address", validators=[DataRequired()])
    pincode = StringField("Pincode", validators=[DataRequired()])
    max_spots = IntegerField("Maximum Spots", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Submit") 