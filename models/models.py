from datetime import datetime
from math import ceil

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from controllers.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")  # 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reservations = db.relationship("Reservation", backref="user", lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        return self.role == "admin"


class ParkingLot(db.Model):
    __tablename__ = "parking_lots"

    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(200), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    max_spots = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    spots = db.relationship("ParkingSpot", backref="lot", lazy=True, cascade="all, delete-orphan")


class ParkingSpot(db.Model):
    __tablename__ = "parking_spots"

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lots.id"), nullable=False)
    status = db.Column(db.String(1), default='A')  # 'A' = Available, 'O' = Occupied
    spot_number = db.Column(db.Integer, nullable=False)

    reservations = db.relationship("Reservation", backref="spot", lazy=True, cascade="all, delete-orphan")


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey("parking_spots.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    parked_at = db.Column(db.DateTime, default=datetime.utcnow)
    released_at = db.Column(db.DateTime, nullable=True)
    total_cost = db.Column(db.Float, nullable=True)

    def close_and_compute_cost(self, price_per_hour: float):
        if not self.released_at:
            self.released_at = datetime.utcnow()
        duration_minutes = (self.released_at - self.parked_at).total_seconds() / 60.0
        hours = duration_minutes / 60.0
        self.total_cost = ceil(hours) * price_per_hour
        return self.total_cost 