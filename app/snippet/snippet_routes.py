from fastapi import APIRouter, FastAPI, Request, HTTPException, Depends
from sqlalchemy.sql.elements import Null

from app.db.base import db, Base
from app.db.schema import Snippet, User
from app.auth.auth_utils import email_verify_token
from slugify import slugify


snippet = APIRouter()

@snippet.post("/create-snippet")
async def create_snippet(payload: dict, user_id=Depends(email_verify_token)):

    title = payload['title']
    desc = payload['desc']
    snippet = payload['snippet']
    language = payload['language']
    theme= payload['theme']

    new_snippet = Snippet(title=title, desc=desc,
                          user_id=user_id, snippet=snippet,language=language,theme=theme)
    if new_snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not created")

    slug = slugify(title)
    new_snippet.url_slug = slug
    new_snippet.insert()
    return {
        "id": new_snippet.snippet_id,
        "message":"success"
    }


@snippet.get("/all-snippets")
async def get_all_snippets():
    result = db.query(Snippet).order_by(Snippet.created_at.desc()).all()
    snippets = [snippet.format() for snippet in result]
    
    
    return {
        "snippets": snippets,
        "message": "success"
    }

@snippet.get("/viewsnippet")
async def get_snippet(snippet_id: int):
    result = db.query(Snippet).filter(Snippet.snippet_id == snippet_id).first()
    user= db.query(User).filter(User.user_id == result.user_id).first()
    snippet = result.format()
    snippet["username"]=user.name
    if result is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet
