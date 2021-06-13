from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.epsode import EpsodeModel

class Epsode(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('serie_id',
        type=int,
        required=True,
        help="this field cannot be left blank!"
    )
    parser.add_argument('season_id',
        type=int,
        required=True,
        help="this field cannot be left blank!"
    )
    parser.add_argument('title', type=str)

    @jwt_required()
    def post(self, number):
        data = Epsode.parser.parse_args()
        serie_id = data['serie_id']
        season_id = data['season_id']

        epsode = EpsodeModel.find_by_serie_id_and_season_id_and_number(serie_id, season_id, number)

        if epsode:
            return {"message": "epsode {}, serie id {} season {} already exists.".format(number, serie_id, season_id)}, 400
        else:
            title = data['title']
            epsode = EpsodeModel(serie_id, season_id, number, title)
            epsode.save_to_db()
            return {"message": "Epsode {} created sucessfully.".format(number)}, 201

    @jwt_required()
    def delete(self, number):
        data = Epsode.parser.parse_args()
        serie_id = data['serie_id']
        season_id = data['season_id']

        epsode = EpsodeModel.find_by_serie_id_and_season_id_and_number(serie_id, season_id, number)

        if epsode:
            epsode.delete()
            return {"message:": "epsode deleted"}, 204
        else:
            return {"message": "couldnt find epsode {}, serie id {} season {}.".format(number, serie_id, season_id)}, 404


class EpsodesList(Resource):

    @jwt_required()
    def get(self):
        epsodes = EpsodeModel.find_all()

        return [epsode.json() for epsode in epsodes]
