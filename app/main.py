from fastapi import FastAPI
from app.routers import auth, users, ideas, comment, upvotes

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ideas.router)
app.include_router(comment.router)
app.include_router(upvotes.router)

@app.get('/')
def index():
    return {'hello': 'world'}