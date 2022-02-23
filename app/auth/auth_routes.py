from fastapi import APIRouter, Header
from fastapi.params import Header

from app.db.base import db
from app.db.schema import User


from datetime import datetime
from werkzeug.security import check_password_hash
import jwt
import datetime

auth = APIRouter()
@auth.post('/signup')
def register_user(payload: dict):

    user = db.query(User).filter_by(email=payload['email']).first()
    if not user:

        new_user = User(payload['name'], payload['email'], payload['password'])
        new_user.insert()

        userid = new_user.user_id

        claims = {
            'id': userid,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        secret_key = 'myprecious'
        auth_token = jwt.encode(claims, secret_key, algorithm='HS256')

        return {
            'success': True,
            'token': auth_token.decode('utf-8'),
            'userInfo': {
                'name': payload['name'],
                'email': payload['email'],
                'user_id': userid
            },
            'user_id': userid,
        }
    else:
        return {
            'message': "User Already exists"
        }


@auth.delete('/delusers')
async def del_users():
    User.delete_all()

    return {
        'message': "success",
        # 'num_users' : users
    }


@auth.post('/loginemail')
def loginemail(payload: dict):
    print(payload)
    user = db.query(User).filter_by(email=payload["email"]).first()
    if user and check_password_hash(user.password, payload["password"]):
        claims = {
            'id': user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        secret_key = 'myprecious'
        auth_token = jwt.encode(claims, secret_key, algorithm='HS256')

        if auth_token:
            return {
                'success': True,
                'token': auth_token.decode('utf-8'),
                'userInfo': {
                    'name': user.name,
                    'email': user.email,
                    'user_id': user.user_id,
                }
            }
    else:
        return {
            'message': "User doesn't exists"
        }
