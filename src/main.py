from fastapi import FastAPI
import uvicorn

from src.api.posts import router as router_posts

app = FastAPI()

app.include_router(router_posts)

if __name__ == "__main__":
    uvicorn.run("main:app")