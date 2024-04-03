from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TelField, ValidationError
from wtforms.validators import Email, Length, EqualTo, InputRequired
from Project.auth.models import User


class LoginForm(FlaskForm):
    email = StringField("E-mailadres:", [InputRequired(
                       message="Dit veld is vereist"),
                       Email(
                             message="Dit is geen geldig email adres, het moet een '@' bevatten")],
                       render_kw={"placeholder": "JohnDoe@gmail.com"})
    wachtwoord = PasswordField("Wachtwoord:", [InputRequired(
                               message="Dit veld is vereist")],
                               render_kw={"placeholder": "********"})
    remember = BooleanField("Onthoud Login:", default="checked")
    submit = SubmitField("Login",
                         render_kw={"class": "btn btn-primary"})


class RegisterForm(FlaskForm):
    email = StringField("E-mailadres:", [InputRequired(
                       message="Dit veld is vereist"),
                       Email(
                             message="Dit is geen geldig email adres, het moet een '@' bevatten")],
                       render_kw={"placeholder": "JohnDoe@gmail.com"})
    wachtwoord = PasswordField("Wachtwoord:", [InputRequired(
                               message="Dit veld is vereist"),
                               Length(min=8, max=30,
                                      message="Wachtwoord moet tussen de 8 en 30 characters lang zijn")],
                               render_kw={"placeholder": "********"})
    rep_wachtwoord = PasswordField("Herhaal WW:", [InputRequired(
                                   message="Dit veld is vereist"),
                                   EqualTo("wachtwoord",
                                           message="Wachtwoorden moeten gelijk aan elkaar zijn")],
                                   render_kw={"placeholder": "********"})
    voornaam = StringField("Naam:", [InputRequired(
                           message="Dit veld is vereist")],
                           render_kw={"placeholder": "John"})
    achternaam = StringField([InputRequired(
                             message="Dit veld is vereist")],
                             render_kw={"placeholder": "Doe"})
    telefoon = TelField("Telefoon:", [InputRequired(
                        message="Dit veld is vereist"),
                        Length(9,
                               message="Het gegeven telefoon nummer is ongeldig")],
                        render_kw={"placeholder": "06 12345678"})
    submit = SubmitField("Registreer",
                         render_kw={"class": "btn btn-primary"})

    def check_email(self, field):
        # Check of het e-mailadres al in de database voorkomt!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')


class ResetRequestForm(FlaskForm):
    email = StringField("E-mailadres:", [InputRequired(
                       message="Dit veld is vereist"),
                       Email(
                            message="Dit is geen geldig email adres, het moet een '@' bevatten")],
                       render_kw={"placeholder": "JohnDoe@gmail.com"})
    submit = SubmitField("Vraag wachtwoord reset aan",
                         render_kw={"class": "btn btn-primary"})


class ResetForm(FlaskForm):
    password = PasswordField("Wachtwoord:", [InputRequired(
                             message="Dit veld is vereist"),
                             EqualTo("rep_password",
                                     message="Wachtwoorden moeten gelijk aan elkaar zijn")],
                             render_kw={"placeholder": "********"})
    rep_password = PasswordField("Wachtwoord Herhalen:", [InputRequired(
                                 message="Dit veld is vereist"),
                                 EqualTo("rep_password",
                                         message="Wachtwoorden moeten gelijk aan elkaar zijn")],
                                 render_kw={"placeholder": "********"})
    submit = SubmitField("Vraag wachtwoord reset aan", render_kw={"class": "btn btn-primary"})
    