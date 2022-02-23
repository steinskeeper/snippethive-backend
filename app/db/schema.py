from sqlalchemy.dialects.postgresql import JSON
from .base import db, Base, engine
from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    BigInteger,
    DateTime,
)
from sqlalchemy.dialects.postgresql import ARRAY, array
from sqlalchemy.orm import relationship

import fity3
import jwt
import json
from werkzeug.security import generate_password_hash
from sqlalchemy.ext.mutable import Mutable

f3 = fity3.generator(1)


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    email = Column(String(150), nullable=False)
    password = Column(String(255), nullable=True)
    picture = Column(String)
    bio = Column(String, default="")

    def __init__(self, name, email, password, picture=None, bio=None):
        self.user_id = next(f3)
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.picture = picture
        self.bio = bio

    def __repr__(self):
        return f"<User id:{self.user_id} name:{self.name}>"

    def encode_auth_token(user_id):
        """Generates the access token."""
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(
                    days=30,
                    seconds=30,
                ),
                "iat": datetime.datetime.utcnow(),
                "sub": str(user_id),
            }
            return jwt.encode(payload, "my_precious", algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the access token - :param auth_token: - :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, "my_precious")
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    def insert(self):
        db.add(self)
        db.commit()

    def update(self):
        db.commit()

    def delete_all():
        db.query(User).delete()
        db.commit()

    def format(self):
        return {
            "name": self.name,
            # "id": self.user_id,
            "email": self.email,
            "picture": self.picture,
            # "password": self.password,
            "bio": self.bio,

        }
        


class Snippet(Base):
    __tablename__ = "snippets"

    snippet_id = Column(BigInteger, primary_key=True, unique=True)
    title = Column(String, nullable=False)
    url_slug = Column(String, nullable=False, primary_key=True)
    desc = Column(String, nullable=False)
    snippet = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    language = Column(String, nullable=True)
    theme = Column(String, nullable=True)

    def __init__(self, title, desc, user_id, snippet, language, theme):
        self.snippet_id = next(f3)
        self.title = title
        self.desc = desc
        # self.url_slug = url_slug
        self.user_id = user_id
        self.snippet = snippet
        self.language = language
        self.theme = theme

    def insert(self):
        db.add(self)
        db.commit()

    def update(self):
        db.commit()

    def delete(self):
        db.delete(self)
        db.commit()

    def delete_all():
        db.query(Snippet).delete()
        db.commit()

    def format(self):
        return {
            "id": (self.snippet_id),
            "title": self.title,
            "desc": self.desc,
            "url_slug": self.url_slug,
            "created_at": self.created_at.strftime("%b %d, %Y"),
            "updated_at": self.updated_at,
            "user_id": str(self.user_id),
            "snippet": self.snippet,
            "language": self.language,
            "theme": self.theme,
        }
