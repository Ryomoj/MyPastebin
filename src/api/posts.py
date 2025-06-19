import hashlib

from fastapi import APIRouter, Query
from sqlalchemy import insert, select, update
import boto3
from starlette.responses import RedirectResponse

from src.database import async_session_maker
from src.models.posts import PostsOrm
from src.schemas.posts import PostAddSchema

router = APIRouter(prefix="/posts", tags=["Блог"])

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

@router.get("/")
async def get_all_posts():
    async with async_session_maker() as s:
        query = select(PostsOrm)
        query_request = await s.execute(query)
        result = query_request.scalars().all()
    return {"Status": "Success", "result": result}


@router.post("/")
async def create_new_post(data: PostAddSchema, key_name = Query(max_length=100)):
    s3.put_object(Bucket='pastebin-s3', Key=key_name, Body=str(data.text))

    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            "Bucket": "pastebin-s3",
            "Key": key_name
        },
        # ExpiresIn=3600  # Время жизни URL в секундах (по умолчанию 3600)
    )

    async with async_session_maker() as s:
        # Добавляем сырой url поста в базу данных
        add_raw_url_stmt = insert(PostsOrm).values(url_s3=url)
        await s.execute(add_raw_url_stmt)

        # Получаем id добавленного поста
        get_post_id = select(PostsOrm).where(PostsOrm.url_s3 == url)
        query_result = await s.execute(get_post_id)
        post = query_result.scalars().one()

        # Получаем хэш от id поста
        sha256_hash = hashlib.new("sha256")
        sha256_hash.update(str(post.id).encode())
        id_hash = sha256_hash.hexdigest()

        # Создаем готовый url с хэшем и добавляем в базу данных
        hashed_url = f"http://127.0.0.1/posts/{id_hash}"
        add_hashed_url_stmt = update(PostsOrm).where(PostsOrm.url_s3 == url).values(url_hashed=hashed_url)
        await s.execute(add_hashed_url_stmt)

        await s.commit()

    return {"Status": "OK", "post_id_hash": hashed_url}

# Ручка для переадресации по хэшированному url
@router.get("/{id_hash}")
async def get_post_by_hashed_url(id_hash):
    async with async_session_maker() as s:
        get_post_by_hashed_url_query = select(PostsOrm.url_s3).where(
            PostsOrm.url_hashed == f"http://127.0.0.1/posts/{id_hash}")
        query_response = await s.execute(get_post_by_hashed_url_query)
        post_url = query_response.scalars().one()

    return RedirectResponse(post_url)


# # Загрузить объекты в бакет
#
# ## Из строки
# s3.put_object(Bucket='pastebin-s3', Key='object_name', Body='TEST', StorageClass='STANDART')
#
#
# # Получить список объектов в бакете
# for key in s3.list_objects(Bucket='bucket-name')['Contents']:
#     print(key['Key'])
#
# # Удалить несколько объектов
# forDeletion = [{'Key':'object_name'}, {'Key':'script/py_script.py'}]
# response = s3.delete_objects(Bucket='bucket-name', Delete={'Objects': forDeletion})
#
# # Получить объект
# get_object_response = s3.get_object(Bucket='bucket-name',Key='py_script.py')
# print(get_object_response['Body'].read())