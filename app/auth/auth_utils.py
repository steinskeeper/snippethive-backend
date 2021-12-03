from fastapi import Request
from app.db.base import db
from app.db.schema import User
import jwt


def email_verify_token(token_jwt: Request):
    token = token_jwt.headers['Authorization']
    print(token)
    data = jwt.decode(token, 'myprecious')

    if (data == None):
        return None

    u_id = data['id']

    userinfo = db.query(User).filter(User.user_id == u_id).first()
    return userinfo.user_id


def getUser(email):
    user = db.query(User).filter(User.email == email).first()
    return user
