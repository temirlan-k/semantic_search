from typing import TYPE_CHECKING
from src.infrastructure.database.models.mixins import Base, AutoincrementIDMixin, TimestampMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
if TYPE_CHECKING:
    from src.infrastructure.database.models.documents import DocumentDBModel


class UserDBModel(Base, AutoincrementIDMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    documents: Mapped[list["DocumentDBModel"]] = relationship(
        "DocumentDBModel", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<UserDBModel id={self.id} username={self.username}>"