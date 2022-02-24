from fastapi import APIRouter, FastAPI, Request, HTTPException, Depends
from sqlalchemy.sql.elements import Null

from app.db.base import db, Base
from app.db.schema import Snippet, User
from app.auth.auth_utils import email_verify_token
from slugify import slugify
from statistics import mode
from sentence_transformers import SentenceTransformer, util
import numpy as np


snippet = APIRouter()


@snippet.post("/create-snippet")
async def create_snippet(payload: dict, user_id=Depends(email_verify_token)):

    title = payload['title']
    desc = payload['desc']
    snippet = payload['snippet']
    language = payload['language']
    theme = payload['theme']

    new_snippet = Snippet(title=title, desc=desc,
                          user_id=user_id, snippet=snippet, language=language, theme=theme)
    if new_snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not created")

    slug = slugify(title)
    new_snippet.url_slug = slug
    new_snippet.insert()
    return {
        "id": new_snippet.snippet_id,
        "message": "success"
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
    dict={}
    corpus=[]
    suggestion_dict={}
    suggest_array=[]
    model = SentenceTransformer("app/aimodel")
    allsnippet = db.query(Snippet).all()
    allsnippets = [snippet.format() for snippet in allsnippet]
    for i in range(len(allsnippets)):
        dict.update({allsnippets[i]['id']: allsnippets[i]['title']})
        corpus.append(allsnippets[i]['title'])
    result = db.query(Snippet).filter(Snippet.snippet_id == snippet_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    user = db.query(User).filter(User.user_id == result.user_id).first()
    sentence = result.title
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    sentence_embedding = model.encode(sentence, convert_to_tensor=True)
    top_k = 3

    cos_scores = util.pytorch_cos_sim(sentence_embedding, corpus_embeddings)[0]

    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
    for idx in top_results[0:top_k]:
        suggest_array.append(idx.item())
    print(suggest_array)
    
    dict_keys=list(dict)
    values=dict.values()
    dict_values=list(values)

    for j in ((suggest_array)):
        suggestion_dict.update({dict_keys[j]: dict_values[j]})
    
    snippet = result.format()
    snippet["username"] = user.name
    snippet["suggestions"] = suggestion_dict
    
    return snippet

@snippet.get("/snippet-suggest")
async def get_snippet_suggest(snippet_id: int):
    dict={}
    corpus=[]
    suggestion_dict={}
    suggest_array=[]
    model = SentenceTransformer("app/aimodel")
    allsnippet = db.query(Snippet).all()
    snippets = [snippet.format() for snippet in allsnippet]
    for i in range(len(snippets)):
        dict.update({snippets[i]['id']: snippets[i]['title']})
        corpus.append(snippets[i]['title'])
    result = db.query(Snippet).filter(Snippet.snippet_id == snippet_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    sentence = result.title
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    sentence_embedding = model.encode(sentence, convert_to_tensor=True)
    top_k = 3

    cos_scores = util.pytorch_cos_sim(sentence_embedding, corpus_embeddings)[0]

    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
    for idx in top_results[0:top_k]:
        suggest_array.append(idx.item())
    print(suggest_array)
    
    dict_keys=list(dict)
    values=dict.values()
    dict_values=list(values)

    for j in ((suggest_array)):
        suggestion_dict.update({dict_keys[j]: dict_values[j]})


    
    return suggestion_dict

@snippet.get("/delete-snippet")
async def delete_snippet(snippet_id: int):
    result = db.query(Snippet).filter(Snippet.snippet_id == snippet_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    result.delete()
    return {"message": "success"}