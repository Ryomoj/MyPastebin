from sqlalchemy import insert, select, update

from src.models.posts import PostsOrm
from src.repositories.base import BaseRepository


class PostsRepository(BaseRepository):
    model = PostsOrm

    async def insert_post_raw_url(self, url):
        add_raw_url_stmt = insert(self.model).values(url_s3=url)
        await self.session.execute(add_raw_url_stmt)


    async def get_post_by_id(self, post_id):
        get_post_query = select(PostsOrm).where(PostsOrm.id == post_id)
        query_result = await self.session.execute(get_post_query)
        post = query_result.scalars().one()
        return post


    async def get_post_by_raw_url(self, url):
        get_post_query = select(PostsOrm).where(PostsOrm.url_s3 == url)
        query_result = await self.session.execute(get_post_query)
        post = query_result.scalars().one()
        return post


    async def get_post_by_hashed_url(self, id_hash):
        get_post_by_hashed_url_query = select(PostsOrm.url_s3).where(
            PostsOrm.url_hashed == f"http://127.0.0.1/posts/{id_hash}")
        query_response = await self.session.execute(get_post_by_hashed_url_query)
        post_hashed_url = query_response.scalars().one()
        return post_hashed_url


    async def insert_complete_post_url(self, url, hashed_url):
        add_hashed_url_stmt = update(PostsOrm).where(PostsOrm.url_s3 == url).values(url_hashed=hashed_url)
        await self.session.execute(add_hashed_url_stmt)
