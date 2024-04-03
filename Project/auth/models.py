from Project import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# De user_loader decorator zorgt voor de flask-login voor de huidige gebruiker
# en haalt zijn/haar id op.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    """Deze class is bedoeld om de gebruikersgegevens op te slaan"""
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    voornaam = db.Column(db.String(24))
    achternaam = db.Column(db.String(24))
    telefoon = db.Column(db.Integer)

    def __init__(self, email, password, voornaam, achternaam, telefoon):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.telefoon = telefoon

    def __repr__(self):
        return (f"persoon gegevens van gebruiker '{self.email}' is:\nid: {self.id}\nvoornaam: {self.voornaam}\n"
                f"achternaam: {self.achternaam}\ntelefoon: {self.telefoon}\npassword hash: {self.password_hash}")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def change_password(self, password):
        self.password_hash = generate_password_hash(password)