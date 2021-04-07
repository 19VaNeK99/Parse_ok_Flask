from main import db, Base
from flask_jwt_extended import create_access_token
from hashlib import md5
from data import Data


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = md5(kwargs.get('password').encode()).hexdigest()

    def get_token(self):
        token = create_access_token(identity=self.id)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if md5(password.encode()).hexdigest() != user.password:
            raise Exception('No user with this password')
        Data.update_login_and_password(user.email, user.password)
        return user
