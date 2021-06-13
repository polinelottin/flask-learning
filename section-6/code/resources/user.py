import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="this field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="this field cannot be left blank!"
    )
    parser.add_argument('email',
        type=str,
        required=True,
        help="this field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'username already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created sucessfully."}, 201

    @jwt_required()
    def get(self):
        user = current_identity
