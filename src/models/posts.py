from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class PostsOrm(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    url_s3: Mapped[str] = mapped_column(String(10840))
    url_hashed: Mapped[str] = mapped_column(String(10840), nullable=True)

