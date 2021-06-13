from flask_restful import Resource
from flask_jwt import jwt_required

from models.serie import SerieModel
from scraping.controller import ScrapController

class Serie(Resource):

    @jwt_required()
    def post(self, name):
        serie = ScrapController.scrap_serie_and_save_to_db(name)

        #mudar aqui... como saber o que foi feito?? retornar um log....
        if serie:
            return {"message": "Serie {} created sucessfully.".format(name)}, 201
        else:
            return {"message": "Server failed to find serie {}. Try another name.".format(name)}, 400

        '''
        serie = SerieModel.find_by_name(name)
        if serie:
            return {"message": "{} already exists.".format(name)}, 400
        else:
            serie = SerieModel(name)
            serie.save_to_db()

            return {"message": "Serie {} created sucessfully.".format(name)}, 201
        '''

    @jwt_required()
    def delete(self, name):
        serie = SerieModel.find_by_name(name)
        if serie:
            serie.delete()
            return {"message:": "serie deleted"}, 204
        else:
            return {"message": "couldnt find serie: {}.".format(name)}, 404


class SeriesList(Resource):
    @jwt_required()
    def get(self):
        series = SerieModel.find_all()

        return [serie.json() for serie in series]
