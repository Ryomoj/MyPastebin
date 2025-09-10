from fastapi import APIRouter, Query
from starlette.responses import RedirectResponse

from src.api.dependencies import DatabaseDep
from src.schemas.posts import PostAddSchema
from src.services.posts import PostService

router = APIRouter(prefix="/posts", tags=["Блог"])


@router.get("/")
async def get_all_posts(
        db: DatabaseDep
):
    return await PostService(db).get_all_posts()


@router.post("/")
async def create_new_post(
        db: DatabaseDep,
        data: PostAddSchema,
        key_name = Query(max_length=100)
):
    return await PostService(db).create_new_post(data=data, key_name=key_name)


@router.get("/{id_hash}")
async def redirect_2_post_by_hashed_url(
        db: DatabaseDep,
        id_hash
):
    post_hashed_url = await PostService(db).get_post_by_hashed_url(id_hash=id_hash)
    return RedirectResponse(post_hashed_url)


@router.delete("/{post_id}")
async def delete_post_by_id(
        db: DatabaseDep,
        post_id: int
):
    return await PostService(db).delete_post_by_id(post_id=post_id)