from db import db

class EpsodeModel(db.Model):
    __tablename__ = 'epsodes'

    id = db.Column(db.Integer, primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(80))

    serie = db.relationship('SerieModel')
    season = db.relationship('SeasonModel', back_populates="epsodes")

    def __init__(self, serie_id, season_id, number, title):
        self.serie_id = serie_id
        self.season_id = season_id
        self.number = number
        self.title = title

    def json(self):
        return {'id': self.id, 'serie_id': self.serie_id, 'season_id': self.season_id, 'number': self.number, 'title': self.title}

    @classmethod
    def find_by_serie_id_and_season_id_and_number(cls, serie_id, season_id, number):
        return cls.query.filter_by(serie_id=serie_id, season_id=season_id, number=number).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
