# this is my view file 
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Booking
from website import db
from datetime import datetime, timedelta

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    delete_past_bookings()  # Clean up past bookings
    posts = Post.query.all()
    bookings = Booking.query.filter_by(user_id=current_user.id).all()  # Retrieve bookings for current user
    return render_template("home.html", user=current_user, bookings=bookings)
@views.route("/book", methods=['POST'])
@login_required
def book():
    delete_past_bookings()  # Clean up past bookings

    if request.method == 'POST':
        booking_date = request.form.get('bookingDate')
        start_time = request.form.get('startTime')
        end_interval = request.form.get('endInterval')

        if booking_date and start_time and end_interval:
            try:
                start_date_time = datetime.strptime(f"{booking_date} {start_time}", "%Y-%m-%d %H:%M")
                end_date_time = start_date_time + timedelta(minutes=int(end_interval))

                existing_bookings = Booking.query.filter(
                    (Booking.start_time < end_date_time) & (Booking.end_time > start_date_time)
                ).all()

                if existing_bookings:
                    flash("This time slot is already booked by another user.", category='error')
                else:
                    new_booking = Booking(start_time=start_date_time, end_time=end_date_time, user_id=current_user.id)
                    db.session.add(new_booking)
                    db.session.commit()
                    flash("Booking successful!", category='success')
            except Exception as e:
                flash(f"An error occurred while booking: {str(e)}", category='error')
        else:
            flash("Please select a date, start time, and an end time interval.", category='error')

    return redirect(url_for('views.home'))


def delete_past_bookings():
    now = datetime.now()
    past_bookings = Booking.query.filter(Booking.end_time < now).all()
    for booking in past_bookings:
        db.session.delete(booking)
    db.session.commit()

