from fastapi import APIRouter,FastAPI, Request, HTTPException, Depends
from sqlalchemy.sql.elements import Null

from app.db.base import db, Base
from app.db.schema import Snippet, User
from app.auth.auth_utils import email_verify_token


user = APIRouter()

