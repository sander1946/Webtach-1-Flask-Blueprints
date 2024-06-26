from Project import db


class BungalowTypes(db.Model):
    """Deze class is bedoeld om de verschillende bungalow types op te slaan"""
    __tablename__ = 'BungalowTypes'

    id = db.Column(db.Integer, primary_key=True)
    aantal = db.Column(db.Integer)
    prijs = db.Column(db.Integer)

    def __init__(self, id, aantal, prijs):
        self.id = id
        self.aantal = aantal
        self.prijs = prijs

    def __repr__(self):
        return f"id: {self.id}\naantal: {self.aantal}\nprijs: {self.prijs}\n"


class BungalowData(db.Model):
    """Deze class is bedoeld om de verschillende bungalows op te slaan"""
    __tablename__ = 'BungalowData'

    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(64))
    type_id = db.Column(db.Integer, db.ForeignKey("BungalowTypes.id"))

    def __init__(self, id, naam, type_id):
        self.id = id
        self.naam = naam
        self.type_id = type_id

    def __repr__(self):
        return f"id: {self.id}\nnaam: {self.naam}\ntype_id: {self.type_id}\n"


class BookingData(db.Model):
    """Deze class is bedoeld om de boekingen van de gebruikers op te slaan"""
    __tablename__ = 'BookingData'

    id = db.Column(db.Integer, primary_key=True)
    gast_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    bungalow_id = db.Column(db.Integer, db.ForeignKey("BungalowData.id"))
    week = db.Column(db.Integer)

    def __init__(self, gast_id, bungalow_id, week):
        self.gast_id = gast_id
        self.bungalow_id = bungalow_id
        self.week = week

    def __repr__(self):
        return f"gast_id: {self.gast_id}\nbungalow_id: {self.bungalow_id}\nweek: {self.week}\n"
    

def populate():
    """Deze functie is bedoeld om de database te vullen met test data."""
    bungalow_type = {"1":[4,280],"2":[6,420],"3":[8,560],"4":[4,360],"5":[6,670],"6":[8,840],"7":[4,520],"8":[6,780]}
    for x in range(1, len(bungalow_type)+1):
        row = BungalowTypes(x, bungalow_type[str(x)][0], bungalow_type[str(x)][1])
        db.session.add(row)
    db.session.commit()
    bungalow_dats = {"1":["De Vlinderchalet","3"],"2":["Zonnestraal Cottage","6"],"3":["Bosrand Retreat","2"],
    "4":["Waterlelie Lodge","5"],"5":["Duinenzicht Villa","8"],"6":["Bloesemhuisje","1"],"7":["Dennenrust Cabin","7"],
    "8":["Merelhuis","4"],"9":["Zonsondergang Haven","2"],"10":["Rivierparel Chalet","5"],"11":["Bergtop Haven","8"],
    "12":["Rustiek Rietdak","1"],"13":["Serenade Cottage","6"],"14":["Oase Bungalow","4"],
    "15":["Knusse Kreekhut","3"],"16":["Panoramaview Lodge","7"],"17":["Avondrood Chalet","2"],
    "18":["Molenzicht Cottage","4"],"19":["Zeegloed Haven","8"],"20":["Vuurvlieg Villa","1"]}
    for x in range(1, len(bungalow_dats)+1):
        row = BungalowData(x, bungalow_dats[str(x)][0], bungalow_dats[str(x)][1])
        db.session.add(row)
    db.session.commit()
    booking = {"1": [1, 1, 1], "2": [2, 2, 12]}
    for x in range(1, len(booking) + 1):
        row = BookingData(booking[str(x)][0], booking[str(x)][1], booking[str(x)][2])
        db.session.add(row)
    db.session.commit()