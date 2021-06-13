import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

class UserModel:
    def __init__(self, _id, username, password, email):
        self.id = _id
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * from users WHERE username=?'
        result = cursor.execute(query, (username,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * from users WHERE id=?'
        result = cursor.execute(query, (id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

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

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO users VALUES(NULL, ?, ?, ?)'
        cursor.execute(query, (data['username'], data['password'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created sucessfully."}, 201

    @jwt_required()
    def get(self):
        user = current_identity
