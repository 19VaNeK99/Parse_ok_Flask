from flask import Flask
from flask_restful import Resource, Api, reqparse
from get_friends import GetFriends
from dotenv import load_dotenv
import os
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager, jwt_required

# load_dotenv()


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

from models import *

Base.metadata.create_all(bind=engine)


class Users(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', required=True, type=int, help="id can't be blank and it be a number")
        self.parser.add_argument('limit', required=True, type=int, help="limit can't be blank and it be a number")
        self.parser.add_argument('timeout', required=True, type=int, help="timeout can't be blank and it be a number")

    decorators = [jwt_required()]

    def get(self):
        args = self.parser.parse_args()
        get_f = GetFriends(timeout=float(args['timeout']))
        result = get_f.parse_friends(id_user=args['id'], limit=int(args['limit']))
        return result


class AuthUsers(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', required=True, type=str, help="email can't be blank and it be not  a number")
        self.parser.add_argument('password', required=True, type=str, help="password can't be blank")

    def post(self):
        args = self.parser.parse_args()
        user = User.authenticate(**args)
        token = user.get_token()
        return {'access_token': token}


class RegisterUsers(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', required=True, type=str, help="name can't be blank")
        self.parser.add_argument('email', required=True, type=str, help="email can't be blank and it be not  a number")
        self.parser.add_argument('password', required=True, type=str, help="password can't be blank")

    def post(self):
        args = self.parser.parse_args()
        user = User(**args)
        session.add(user)
        session.commit()
        token = user.get_token()
        return {'access_token': token}


api.add_resource(Users, '/api/users')

api.add_resource(AuthUsers, '/api/login')
api.add_resource(RegisterUsers, '/api/register')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
