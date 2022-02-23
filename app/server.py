from fastapi import FastAPI
from app.auth.auth_routes import auth
from app.snippet.snippet_routes import snippet
from app.user.user_routes import user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(snippet)
app.include_router(user)


@app.get("/")
async def root():
    type = "hello"
    return {"message": "Hello World",
            "type": type}
