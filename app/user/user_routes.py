from fastapi import APIRouter,FastAPI, Request, HTTPException, Depends
from sqlalchemy.sql.elements import Null

from app.db.base import db, Base
from app.db.schema import Snippet, User
from app.auth.auth_utils import email_verify_token


user = APIRouter()
@user.get("/user-info")
async def get_user(user_id: int):
    result = db.query(Snippet).filter(Snippet.user_id == user_id).all()
    user= db.query(User).filter(User.user_id == user_id).first()
    snippets = [snippet.format() for snippet in result]
    
    if result is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return {
        "snippets": snippets,
        "user": user
    }

