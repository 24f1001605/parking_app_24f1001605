from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from .extensions import db
from models.models import ParkingLot, ParkingSpot, Reservation
from sqlalchemy import func

user_bp = Blueprint("user", __name__, template_folder="../templates/user")


@user_bp.route("/dashboard")
@login_required
def dashboard():
    # active booking
    active_res = (Reservation.query
                  .filter_by(user_id=current_user.id, released_at=None)
                  .order_by(Reservation.parked_at.desc())
                  .first())

    # history
    history = (Reservation.query
               .filter(Reservation.user_id == current_user.id, Reservation.released_at.isnot(None))
               .order_by(Reservation.parked_at.desc())
               .all())

    # chart data: usage history per lot (sum of total_cost)
    chart_labels = []
    chart_values = []
    rows = (db.session.query(ParkingLot.prime_location_name, func.sum(Reservation.total_cost))
            .join(ParkingSpot, ParkingSpot.lot_id == ParkingLot.id)
            .join(Reservation, Reservation.spot_id == ParkingSpot.id)
            .filter(Reservation.user_id == current_user.id, Reservation.total_cost.isnot(None))
            .group_by(ParkingLot.id)
            .all())
    for name, total in rows:
        chart_labels.append(name)
        chart_values.append(float(total or 0.0))

    lots = ParkingLot.query.order_by(ParkingLot.prime_location_name).all()
    return render_template("user/dashboard.html",
                           active_res=active_res,
                           history=history,
                           lots=lots,
                           chart_labels=chart_labels,
                           chart_values=chart_values)


@user_bp.route("/book", methods=["POST"])
@login_required
def book():
    lot_id = request.form.get("lot_id", type=int)
    if lot_id is None:
        flash("Invalid lot.", "danger")
        return redirect(url_for("user.dashboard"))

    # Rule: user can have only one active reservation
    active = Reservation.query.filter_by(user_id=current_user.id, released_at=None).first()
    if active:
        flash("You already have an active reservation.", "warning")
        return redirect(url_for("user.dashboard"))

    lot = ParkingLot.query.get_or_404(lot_id)
    # First available spot
    spot = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').order_by(ParkingSpot.spot_number.asc()).first()
    if not spot:
        flash("No available spots in the selected lot.", "danger")
        return redirect(url_for("user.dashboard"))

    spot.status = 'O'
    res = Reservation(spot_id=spot.id, user_id=current_user.id, parked_at=datetime.utcnow())
    db.session.add(res)
    db.session.commit()
    flash(f"Spot #{spot.spot_number} allocated in lot {lot.prime_location_name}.", "success")
    return redirect(url_for("user.dashboard"))


@user_bp.route("/release/<int:reservation_id>", methods=["POST"])
@login_required
def release(reservation_id):
    res = Reservation.query.get_or_404(reservation_id)
    if res.user_id != current_user.id and not current_user.is_admin():
        abort(403)
    if res.released_at:
        flash("Reservation already released.", "info")
        return redirect(url_for("user.dashboard"))

    lot = res.spot.lot
    res.close_and_compute_cost(lot.price_per_hour)
    res.spot.status = 'A'
    db.session.commit()
    flash(f"Reservation released. Total cost: {res.total_cost:.2f}", "success")
    if current_user.is_admin():
        return redirect(url_for("admin.dashboard"))
    return redirect(url_for("user.dashboard")) 