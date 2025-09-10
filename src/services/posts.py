import hashlib
from urllib.parse import urlparse

from src.config.config import s3
from src.schemas.posts import PostAddSchema
from src.services.base import BaseService


class PostService(BaseService):
    async def get_all_posts(self):
        return await self.db.posts.get_all()


    async def create_new_post(self, data: PostAddSchema, key_name):

        # Суем пост в бакет S3 хранилища
        s3.put_object(Bucket='pastebin-s3', Key=key_name, Body=str(data.text))

        # Получаем URL добавленного
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                "Bucket": "pastebin-s3",
                "Key": key_name
            },
            # ExpiresIn=3600 # Время жизни URL в секундах (по умолчанию 3600)
        )

        # Добавляем сырой url поста в базу данных
        await self.db.posts.insert_post_raw_url(url=url)
        await self.db.commit()

        # Получаем id добавленного поста
        post = await self.db.posts.get_post_by_raw_url(url=url)

        # Получаем хэш от id поста
        sha256_hash = hashlib.new("sha256")
        sha256_hash.update(str(post.id).encode())
        id_hash = sha256_hash.hexdigest()

        # Создаем готовый url с хэшем и добавляем в базу данных
        hashed_url = f"http://127.0.0.1/posts/{id_hash}"
        await self.db.posts.insert_complete_post_url(url=url, hashed_url=hashed_url)
        await self.db.commit()

        return {"Status": "OK", "hashed_url": hashed_url}


    async def get_post_by_hashed_url(self, id_hash):
        return await self.db.posts.get_post_by_hashed_url(id_hash=id_hash)


    async def delete_post_by_id(self, post_id):
        post = await self.db.posts.get_post_by_id(post_id=post_id)

        parsed_url = urlparse(post.url_s3)
        key_name = parsed_url.path.lstrip('/')

        s3.delete_object(Bucket='pastebin-s3', Key=key_name)

        await self.db.posts.delete(id=post_id)
        await self.db.commit()

        return {"Status": "OK"}