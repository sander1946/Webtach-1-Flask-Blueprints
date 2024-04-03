# local imports
from Project.home import blueprint

# flask imports
from flask import render_template, redirect, url_for, flash, request


@blueprint.route('/', methods=["GET"])
def index():
    """Deze functie wordt aangeroepen als de user naar de home pagina gaat"""
    return render_template("home/index.html")


@blueprint.route('/feedback', methods=["POST"])
def feedback():
    """ Deze functie wordt aangeroepen als de user feedback geeft, stuur een flash message en
        stuurt de user terug naar de pagina waar ze vandaan kwamen of weer naar de home pagina"""
    if request.method == "POST":
        flash(f"Het bericht is verzonden!")
        next_page = request.args.get("next")
        if next_page is not None:
            return redirect(next_page)
    return redirect(url_for("home_blueprint.index"))