from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, HiddenField
from wtforms.validators import InputRequired
from Project.boeking.models import BookingData
from flask import request


class BoekForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url = request.path
        url = url.split("/")
        token = url[-1]
        data = BookingData.query.with_entities(BookingData.week).filter_by(bungalow_id=token)
        weeks = []
        for week in data:
            weeks.append(week[0])
        self.week.choices = [x for x in range(1, 53) if x not in weeks]

    week = SelectField("Welke Week?: ", [InputRequired(message="Dit veld is vereist")], coerce=int)
    submit = SubmitField("Boek Bungalow",
                         render_kw={"class": "btn btn-primary"})


class WijzigForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url = request.path
        url = url.split("/")
        bungalow = url[-2]
        data = BookingData.query.with_entities(BookingData.week).filter_by(bungalow_id=bungalow)
        weeks = []
        for week in data:
            weeks.append(week[0])
        coises = [x for x in range(1, 53) if x not in weeks]
        self.week.choices = coises

    week = SelectField("Nieuwe Week?: ", [InputRequired(message="Dit veld is vereist")], coerce=int)
    submit = SubmitField("Verander Boeking",
                         render_kw={"class": "btn btn-primary"})


class AnnuleerForm(FlaskForm):
    confirm = SelectField("Weet je het zeker?: ", [InputRequired(message="Dit veld is vereist")], choices=["Nee", "Ja"], coerce=str)
    submit = SubmitField("Bevestig",
                         render_kw={"class": "btn btn-primary"})
    

class WijzigBungalowForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bungalow_id.render_kw = {"value": kwargs["bungalow"]}

    bungalow_id = HiddenField(render_kw={"value": 0})
    boek = SubmitField("Boek deze bungalow",
                         render_kw={"class": "btn btn-primary"})
