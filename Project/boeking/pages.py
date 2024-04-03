# local imports
from Project import db
from Project.boeking import blueprint
from Project.boeking.forms import BoekForm, WijzigForm, AnnuleerForm, WijzigBungalowForm
from Project.boeking.models import BungalowData, BungalowTypes, BookingData, populate

# flask imports
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

# python imports
from random import randint, choice
import datetime


@blueprint.route('/boek', methods=["GET"])
@login_required
def boek_inv():
    """Deze functie wordt aangeroepen als de user naar de boek pagina gaat zonder een bungalow te selecteren"""
    return redirect(url_for("boeking_blueprint.bungalows"))


@blueprint.route('/boek/<token>', methods=["GET", "POST"])
@login_required
def boek(token):
    """Deze functie wordt aangeroepen als de user naar de boek pagina gaat met een bungalow id in de url"""
    form = BoekForm(week=datetime.date.today().isocalendar().week)
    bungalow = []
    bungalows_info = (db.session.query(BungalowData, BungalowTypes).join(BungalowTypes)
                      .filter(BungalowData.id == token).first())
    # check of de bungalow id klopt
    if bungalows_info:
        data, types = bungalows_info
        bungalow_info = {"img": "/static/img/stock.png", "title": data.naam, "prijs": types.prijs,
                         "aantal_pers": types.aantal, "grote": randint(types.aantal * 45, types.aantal * 55),
                         "opmerking": choice(["Knus", "Sfeervol", "Comfortabel", "Rustiek", "Modern", "Landelijk",
                                              "Praktisch", "Gezellig", "Stijlvol", "Duurzaam"]), "id": data.id}
        bungalow.append(bungalow_info)
        if form.validate_on_submit():
            # check of de form is beantwoord (POST request)
            week = form.week.data
            user_id = current_user.id
            geboekt = BookingData(user_id, token, week)
            db.session.add(geboekt)
            db.session.commit()
            flash(f"Bungalow '{data.naam}' is geboekt voor week {week}")
            return redirect(url_for("boeking_blueprint.boekingen"))
        # als de form niet is beantwoord (GET request)
        return render_template("boeking/boek.html", bungalow_data=bungalow, form=form,
                               week=datetime.date.today().isocalendar().week)
    else:
        # als de bungalow id niet klopt
        return redirect(url_for("boeking_blueprint.bungalows"))
    

@blueprint.route('/boek/<bungalow>/<token>', methods=["GET", "POST"])
@login_required
def wijzigBungalow(bungalow, token):
    forms = []
    booking = BookingData.query.filter_by(id=token).first()
    bungalow_lijst = []
    booking_data_sub = db.session.query(BookingData.bungalow_id).filter(BookingData.week == booking.week)
    bungalows = db.session.query(BungalowData, BungalowTypes).join(BungalowTypes).filter(BungalowData.id.notin_(booking_data_sub)).all()
    if bungalows:
        for data, types in bungalows:
            form = WijzigBungalowForm(bungalow = data.id)
            bungalow_info = {"img": "/static/img/stock.png", "title": data.naam, "prijs": types.prijs,
                                "aantal_pers": types.aantal, "grote": randint(types.aantal * 45, types.aantal * 55),
                                "opmerking": choice(["Knus", "Sfeervol", "Comfortabel", "Rustiek", "Modern", "Landelijk",
                                                    "Praktisch", "Gezellig", "Stijlvol", "Duurzaam"]), "id": data.id, "form": form}
            bungalow_lijst.append(bungalow_info)
            if form.validate_on_submit():
                # check of de form is beantwoord (POST request)
                boeking_new = BookingData.query.get(token)
                boeking_new.bungalow_id = form.bungalow_id.data
                db.session.add(boeking_new)
                db.session.commit()
                flash(f"Bungalow: '{data.naam}' geboekt door: {current_user.email}")
                return redirect(url_for("boeking_blueprint.boekingen"))
            # als de form niet is beantwoord (GET request)
    else:
        flash("Er zijn geen bungalows beschikbaar voor deze week!", "error")
        return redirect(url_for("boeking_blueprint.boekingen"))

    # laat alle bungalows zien die in de database staan
    return render_template("boeking/wijzigBungalow.html", bungalow_data=bungalow_lijst, forms=forms)


@blueprint.route('/boekingen', methods=["GET"])
@login_required
def boekingen():
    """Deze functie wordt aangeroepen als de user naar de boekingen pagina gaat, en geeft de boekingen van de user weer"""
    bungalow = []
    booking_info = (db.session.query(BookingData, BungalowData, BungalowTypes).select_from(BookingData).
                    join(BungalowTypes, BookingData.bungalow_id == BungalowData.id)
                    .join(BungalowData, BungalowData.type_id == BungalowTypes.id)
                    .filter(BookingData.gast_id == current_user.id).order_by(BookingData.week.asc()).all())
    if booking_info:
        # check of de user boekingen heeft
        for bookings, data, types in booking_info:
            bungalow_info = {"img": "/static/img/stock.png", "title": data.naam, "prijs": types.prijs,
                             "aantal_pers": types.aantal, "grote": randint(types.aantal * 45, types.aantal * 55),
                             "opmerking": choice(["Knus", "Sfeervol", "Comfortabel", "Rustiek", "Modern", "Landelijk",
                                                  "Praktisch", "Gezellig", "Stijlvol", "Duurzaam"]), "id": data.id,
                             "week": bookings.week, "booking_id": f"{data.id}/{bookings.id}"}
            bungalow.append(bungalow_info)
        return render_template("boeking/boekingen.html", bungalow_data=bungalow,
                               week=datetime.date.today().isocalendar().week)
    else:
        # als de user geen boekingen heeft
        return render_template("boeking/boekingen.html")


@blueprint.route('/wijzig', methods=["GET"])
@login_required
def wijzig_inv():
    """Deze functie wordt aangeroepen als de user naar de wijzig pagina gaat zonder een bungalow te selecteren"""
    return redirect(url_for("boeking_blueprint.boekingen"))


@blueprint.route('/wijzig/<bungalow>', methods=["GET"])
@login_required
def wijzig_inv_inv():
    """Deze functie wordt aangeroepen als de user naar de wijzig pagina gaat zonder een booking token te selecteren"""
    return redirect(url_for("boeking_blueprint.boekingen"))


@blueprint.route('/wijzig/<bungalow>/<token>', methods=["GET", "POST"])
@login_required
def wijzig(bungalow, token):
    """Deze functie wordt aangeroepen als de user naar de wijzig pagina gaat met een bungalow en booking token in de url"""
    form = WijzigForm(week=datetime.date.today().isocalendar().week)
    bungalow = []
    booking_info = (db.session.query(BookingData, BungalowData, BungalowTypes).select_from(BookingData).
                    join(BungalowTypes, BookingData.bungalow_id == BungalowData.id)
                    .join(BungalowData, BungalowData.type_id == BungalowTypes.id).filter(BookingData.id == token)
                    .first())
    if booking_info:
        # check of de booking token klopt
        bookings, data, types = booking_info
        bungalow_info = {"img": "/static/img/stock.png", "title": data.naam, "prijs": types.prijs,
                         "aantal_pers": types.aantal, "grote": randint(types.aantal * 45, types.aantal * 55),
                         "opmerking": choice(["Knus", "Sfeervol", "Comfortabel", "Rustiek", "Modern", "Landelijk",
                                              "Praktisch", "Gezellig", "Stijlvol", "Duurzaam"]), "id": data.id,
                         "week": bookings.week}
        bungalow.append(bungalow_info)
        if form.validate_on_submit():
            # check of de form is beantwoord (POST request)
            week = form.week.data
            if week == "annuleer boeking":
                # check of de user de boeking wilt annuleren
                flash(f"Boeking van bungalow '{data.naam}' is geannuleerd voor week {week}")
                boeking_new = BookingData.query.get(token)
                db.session.delete(boeking_new)
                db.session.commit()
                return redirect(url_for("boeking_blueprint.boekingen"))
            else:
                # check of de user de boeking week wilt wijzigen
                boeking_new = BookingData.query.get(token)
                boeking_new.week = week
                db.session.add(boeking_new)
                db.session.commit()
                flash(f"Bungalow: '{data.naam}' geboekt voor week: {week} door: {current_user.email}")
                return redirect(url_for("boeking_blueprint.boekingen"))
        # als de form niet is beantwoord (GET request)
        return render_template("boeking/wijzig.html", bungalow_data=bungalow, form=form,
                               week=datetime.date.today().isocalendar().week)
    else:
        # als de booking token niet klopt
        return render_template("boeking/wijzig.html")


@blueprint.route('/annuleer', methods=["GET"])
@login_required
def annuleer_inv():
    """Deze functie wordt aangeroepen als de user naar de annuleer pagina gaat zonder een bungalow te selecteren"""
    return redirect(url_for("boeking_blueprint.boekingen"))


@blueprint.route('/annuleer/<bungalow>', methods=["GET"])
@login_required
def annuleer_inv_inv():
    """Deze functie wordt aangeroepen als de user naar de annuleer pagina gaat zonder een booking token te selecteren"""
    return redirect(url_for("boeking_blueprint.boekingen"))


@blueprint.route('/annuleer/<bungalow>/<token>', methods=["GET", "POST"])
@login_required
def annuleer(bungalow, token):
    """Deze functie wordt aangeroepen als de user naar de annuleer pagina gaat met een bungalow en booking token in de url"""
    form = AnnuleerForm()
    bungalow = []
    booking_info = (db.session.query(BookingData, BungalowData, BungalowTypes).select_from(BookingData).
                    join(BungalowTypes, BookingData.bungalow_id == BungalowData.id)
                    .join(BungalowData, BungalowData.type_id == BungalowTypes.id).filter(BookingData.id == token)
                    .first())
    if booking_info:
        # check of de booking token klopt
        bookings, data, types = booking_info
        bungalow_info = {"img": "/static/img/stock.png", "title": data.naam, "prijs": types.prijs,
                         "aantal_pers": types.aantal, "grote": randint(types.aantal * 45, types.aantal * 55),
                         "opmerking": choice(["Knus", "Sfeervol", "Comfortabel", "Rustiek", "Modern", "Landelijk",
                                              "Praktisch", "Gezellig", "Stijlvol", "Duurzaam"]), "id": data.id,
                         "week": bookings.week}
        bungalow.append(bungalow_info)
        if form.validate_on_submit():
            # check of de form is beantwoord (POST request)
            confirm = form.confirm.data
            if confirm == "Ja":
                # check of de user de boeking wilt annuleren
                flash(f"Boeking van bungalow '{data.naam}' is geannuleerd voor week {bookings.week}")
                boeking_new = BookingData.query.get(token)
                db.session.delete(boeking_new)
                db.session.commit()
                return redirect(url_for("boeking_blueprint.boekingen"))
            else:
                # check of de user de boeking wilt behouden
                flash(f"Bungalow: '{data.naam}' is niet geannuleerd!", "info")
                return redirect(url_for("boeking_blueprint.boekingen"))
        # als de form niet is beantwoord (GET request)
        return render_template("boeking/annuleer.html", bungalow_data=bungalow, form=form,
                               week=datetime.date.today().isocalendar().week)
    else:
        # als de booking token niet klopt
        return redirect(url_for("boeking_blueprint.boekingen"))


@blueprint.route('/bungalows', methods=["GET"])
def bungalows():
    """Deze functie wordt aangeroepen als de user naar de bungalows pagina gaat, en geeft de bungalows weer"""
    bungalow_lijst = []
    bungalow = db.session.query(BungalowData, BungalowTypes).join(BungalowTypes).all()
    if not bungalow:
        # check of de database leeg is (voor testen)
        populate()
        flash("De database is weer gevuld, herlaad de pagina als je niks ziet!", "error")
        return redirect(url_for("boeking_blueprint.bungalows"))
    for data, types in bungalow:
        bungalow_dat = {"img": "/static/img/stock.png", "title": data.naam, "prijs": types.prijs,
                        "aantal_pers": types.aantal, "grote": randint(types.aantal * 45, types.aantal * 55),
                        "opmerking": choice(["Knus", "Sfeervol", "Comfortabel", "Rustiek", "Modern", "Landelijk",
                                             "Praktisch", "Gezellig", "Stijlvol", "Duurzaam"]), "id": data.id}
        bungalow_lijst.append(bungalow_dat)
    # laat alle bungalows zien die in de database staan
    return render_template("boeking/bungalows.html", bungalow_data=bungalow_lijst)