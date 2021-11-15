from flask import render_template, redirect
from flask.helpers import url_for
from controllers import get_agencies, get_trips
from settings import app
from forms import AddAgencyForm, AddTripForm
from models import db, Agency, Trip

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ceļojumi')
def celojumi():
    return render_template("celojumi.html", trips = get_trips())

@app.route('/admin')
def admin():
    return redirect(url_for("admin_agencies"))

@app.route('/profils')
def profils():
    return render_template("profile.html")

@app.route('/admin/agencies')
def admin_agencies():
    return render_template("templates/agencies.html", agencies = get_agencies())

@app.route('/admin/trips')
def admin_trips():
    return render_template("templates/trips.html", trips = get_trips(), agencies = get_agencies())

@app.route('/admin/add')
def admin_add():
    return redirect(url_for("admin_add_agencies"))

@app.route('/admin/add/agencies', methods=['GET', 'POST'])
def admin_add_agencies():
    form = AddAgencyForm()
    if form.validate_on_submit():
        # --Gundars
        # Vēlāk šeit (un admin_add_trips()) tiks pievienotas datu pārbaudes
        # Pagaidām, lai būtu iespējams strādāt ar datiem, atstāšu tīrus inputus
        agency = Agency(name=form.name.data, address=form.address.data, number=form.phone_number.data)
        db.session.add(agency)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template("templates/add_agency.html", form=form)

@app.route('/admin/add/trips', methods=['GET', 'POST'])
def admin_add_trips():
    form = AddTripForm()
    if form.validate_on_submit():
        # Pārbaude
        agency = Agency.query.filter_by(name=form.agency.data).first().id
        trip = Trip(
            agency_id=agency,
            country_from=form.country_from.data,
            country_to=form.country_to.data,
            date_from=form.date_from.data,
            date_to=form.date_to.data,
            description=form.description.data,
            cost=form.cost.data,
            ticket_amount=form.ticket_amount.data,
            views=0 )
        db.session.add(trip)
        db.session.commit()
        return redirect(url_for('admin_trips'))
    return render_template("templates/add_trip.html", form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
