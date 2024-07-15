from fastapi import FastAPI
import uvicorn

app = FastAPI(title="FastAPI with SQLAlchemy Async", version="0.1.0")


@app.get("/", summary="Root Endpoint", description="This is the root endpoint of the API.")
async def root():
    return {"message": "Hello Guys!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
