from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, timedelta

from security import authenticate, identity
from models.user import UserRegister
from models.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity) # /auth

app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800) #half hour
#sapp.config['JWT_AUTH_USERNAME_KEY'] = 'email' #instead username

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

'''
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                    'access_token': access_token.decode('utf-8'),
                    'user_id': identity.id
                    }), error.status_code
'''

#se importar o arquivo app nao run de novo
#so roda se for linha de comando, aih name eh o main (python app.py)
if __name__ == '__main__':
    app.run(port=5000, debug=True)
