from db import db

class SeasonModel(db.Model):
    __tablename__ = 'seasons'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer)

    serie = db.relationship('SerieModel', back_populates="seasons")
    epsodes = db.relationship("EpsodeModel", back_populates="season", cascade="save-update, merge, delete")

    def __init__(self, serie_id, number, year):
        self.serie_id = serie_id
        self.number = number
        self.year = year

    def json(self):
        return {'id': self.id, 'serie_id': self.serie_id, 'number': self.number, 'year': self.year,
            'epsodes': [epsode.json() for epsode in self.epsodes]}

    @classmethod
    def find_by_serie_id_and_number(cls, serie_id, number):
        return cls.query.filter_by(serie_id=serie_id, number=number).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
