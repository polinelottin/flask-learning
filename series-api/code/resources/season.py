from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.season import SeasonModel

class Season(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('number',
        type=int,
        required=True,
        help="this field cannot be left blank!"
    )
    parser.add_argument('year', type=int)

    @jwt_required()
    def post(self, serie_id):
        data = Season.parser.parse_args()
        number = data['number']
        year = data['year']

        season = SeasonModel.find_by_serie_id_and_number(serie_id, number)

        if season:
            return {"message": "season number {} already exists.".format(number)}, 400
        else:
            season = SeasonModel(serie_id, number, year)
            season.save_to_db()
            return {"message": "Season number {} created sucessfully.".format(number)}, 201

    @jwt_required()
    def delete(self, serie_id):
        data = Season.parser.parse_args()
        number = data['number']
        year = data['year']

        season = SeasonModel.find_by_serie_id_and_number(serie_id, number)

        if season:
            season.delete()
            return {"message:": "season deleted"}, 204
        else:
            return {"message": "couldnt find season number {}, serie id {}.".format(number, serie_id)}, 404


class SeasonList(Resource):

    @jwt_required()
    def get(self):
        seasons = SeasonModel.find_all()

        return [season.json() for season in seasons]
