from sqlalchemy import select, delete


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self) -> list:
        query = select(self.model)
        query_request = await self.session.execute(query)
        result = query_request.scalars().all()
        return [post for post in result]

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)