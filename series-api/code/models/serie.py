from db import db

class SerieModel(db.Model):
    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    IMDB_id = db.Column(db.String(80), nullable=False)

    seasons = db.relationship("SeasonModel", back_populates="serie", cascade="save-update, merge, delete")

    def __init__(self, name, IMDB_id):
        self.name = name
        self.IMDB_id = IMDB_id

    def json(self):
        return {'id': self.id, 'name': self.name,
            'seasons': [season.json() for season in self.seasons]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
