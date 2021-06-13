from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT, timedelta

from security import authenticate, identity
from resources.user import UserRegister
from resources.serie import Serie, SeriesList
from resources.season import Season, SeasonList
from resources.epsode import Epsode, EpsodesList

app = Flask(__name__)
app.secret_key = "chilli"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800) #half hour
app.config['JWT_AUTH_URL_RULE'] = '/login'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

#o ideal eh colocar em outro app dps
@app.route('/')
def home():
    return render_template("index.html")

api.add_resource(UserRegister, '/register')
api.add_resource(Serie, '/series/<string:name>')
api.add_resource(SeriesList, '/series')
api.add_resource(Season, '/seasons/<int:serie_id>')
api.add_resource(SeasonList, '/seasons')
api.add_resource(Epsode, '/epsodes/<int:number>')
api.add_resource(EpsodesList, '/epsodes')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
