from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from Project import db
from Project.auth import blueprint
from Project.auth.forms import LoginForm, RegisterForm, ResetRequestForm, ResetForm
from Project.auth.models import User


@blueprint.route('/logout', methods=["GET"])
@login_required
def logout():
    """Deze functie wordt aangeroepen als de user uitlogt en stuur een flash message"""
    logout_user()
    flash('Je bent nu uitgelogd!', 'info')
    return redirect(url_for("home_blueprint.index"))


@blueprint.route('/login', methods=["GET", "POST"])
def login():
    """Deze functie wordt aangeroepen als de user naar de login pagina gaat.
    Als de user al is ingelogd word hij naar de home pagina toe gestuurd"""
    form = LoginForm()
    # check of de user al is ingelogd
    if current_user.is_authenticated:
        flash(f"Je bent al ingelogd!", "info")
        return redirect(url_for("home_blueprint.index"))
    # check of de form is beantwoord (POST request)
    if form.validate_on_submit():
        # check of de form is ingevuld
        if form.email.data != "" and form.wachtwoord.data != "":
            user = User.query.filter_by(email=form.email.data).first()
            # check of de email is geregistreerd
            if user is None:
                flash(f"De email en/of wachtwoord is incorrect! "
                      f"Vraag een nieuw wachtwoord aan als je deze bent vergeten!", "error")
                return redirect(url_for("auth_blueprint.login"))
            # check of het wachtwoord klopt
            if user.check_password(form.wachtwoord.data) and user is not None:
                login_user(user, remember=form.remember.data)
                flash(f"Succesvol ingelogd!", "info")
                # Als de user van een andere pagina komt dan de login pagina, stuur hem dan terug naar die pagina
                next_page = request.args.get('next')
                if next_page is None or not next_page[0] == '/':
                    next_page = url_for("boeking_blueprint.bungalows")
                return redirect(next_page)
            else:
                # als het wachtwoord niet klopt
                flash(f"De email en/of wachtwoord is incorrect! "
                      f"Vraag een nieuw wachtwoord aan als je deze bent vergeten!", "error")
                return redirect(url_for("auth_blueprint.login"))
        else:
            # de email en/of wachtwoord niet is ingevuld
            flash("Vul een geldig e-mailadres en wachtwoord in!", "error")
            return redirect(url_for("auth_blueprint.login"))
    else:
        # als de form niet is beantwoord (GET request)
        return render_template("auth/login.html", form=form)


@blueprint.route('/register', methods=["GET", "POST"])
def register():
    """Deze functie wordt aangeroepen als de user naar de register pagina gaat"""
    form = RegisterForm()
    # check of de form is beantwoord (POST request)
    if form.validate_on_submit():
        # check of de form is ingevuld
        if (form.email.data != "" and form.wachtwoord.data != "" and form.voornaam.data != ""
                and form.achternaam.data != "" and form.telefoon.data != ""):
            user = User.query.filter_by(email=form.email.data)
            # check of de email al is geregistreerd
            if not user.all():
                new_cur = User(email=form.email.data,
                               password=form.wachtwoord.data,
                               voornaam=form.voornaam.data,
                               achternaam=form.achternaam.data,
                               telefoon=form.telefoon.data)
                db.session.add(new_cur)
                db.session.commit()
                flash("Successfully registered, je kunt nu inloggen!", "info")
                return redirect(url_for("auth_blueprint.login"))
            else:
                # als de email al is geregistreerd
                flash("Deze email is al geregistreerd! Log in plaats daarvan in!", "error")
                return redirect(url_for("auth_blueprint.login"))
        else:
            # als de form niet is ingevuld
            flash("Alle gegevens moeten in gevuld zijn!", "error")
            return redirect(url_for("auth_blueprint.register"))
    else:
        # als de form niet is beantwoord (GET request)
        return render_template("auth/register.html", form=form)


@blueprint.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    """Deze functie wordt aangeroepen als de user naar de reset password pagina gaat"""
    form = ResetRequestForm()
    # check of de form is beantwoord (POST request)
    if form.validate_on_submit():
        # check of de form is ingevuld
        if form.email.data != "":
            user = User.query.filter_by(email=form.email.data)
            if not user.all():
                # als de email niet is geregistreerd
                flash(f"Dit email heeft geen nog geen account, maak er een aan!", "error")
                return redirect(url_for("auth_blueprint.register"))
            if user.first():
                # als de email is geregistreerd
                link = f"/reset_password/{user.first().id}"
                flash(f'Wachtwoord reset voor het account: {form.email.data} is aangevraagd.\n'
                      f'De link is: ', link)
                return redirect(url_for("auth_blueprint.reset_password"))
        else:
            # als de form niet is ingevuld
            flash("Vul een geldig email en wachtwoord in!", "error")
            return redirect(url_for("auth_blueprint.reset_password"))
    else:
        # als de form niet is beantwoord (GET request)
        return render_template("auth/reset_password_request.html", form=form)


@blueprint.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_password_token(token):
    """Deze functie wordt aangeroepen als de user daadwerkelijk een wachtwoord reset link bezoekt"""	
    form = ResetForm()
    user = User.query.filter_by(id=token)
    # check of de token klopt
    if user.all():
        # check of de form is beantwoord (POST request)
        if form.validate_on_submit():
            if form.password.data == form.rep_password.data:
                # als de wachtwoorden overeen komen
                user = User.query.get(token)
                user.change_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash("Wachtwoord succesvol gereset!", "info")
                return redirect(url_for("auth_blueprint.login"))
            else:
                # als de wachtwoorden niet overeen komen
                flash("De wachtwoorden komen niet overeen!", "error")
                return redirect(url_for("auth_blueprint.reset_password"))
        # als de form niet is beantwoord (GET request)
        return render_template("auth/reset_password.html", form=form)
    else:
        # als de token niet klopt
        flash("Ongeldige link!", "error")
        return redirect(url_for("auth_blueprint.reset_password"))