from fastapi import FastAPI
import uvicorn

from src.post.routers import router as posts_router
from src.auth.routers import router as auth_router
from src.user.routers import router as user_router

app = FastAPI(title="FastAPI with SQLAlchemy Async", version="0.1.0")

app.include_router(router=posts_router, prefix="/posts")
app.include_router(router=user_router, prefix="/user")
app.include_router(router=auth_router, prefix="/oauth2")


@app.get("/", summary="Root Endpoint", description="This is the root endpoint of the API.")
async def root():
    return {"message": "Hello Guys!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
