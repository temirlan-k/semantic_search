from typing import TYPE_CHECKING
from src.infrastructure.database.models.mixins import (
    Base,
    AutoincrementIDMixin,
    TimestampMixin,
    UUIDMixin,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

if TYPE_CHECKING:
    from src.infrastructure.database.models.users import UserDBModel


class DocumentDBModel(Base, AutoincrementIDMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "documents"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    filename: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False)
    chunk_size: Mapped[int] = mapped_column(nullable=False)
    chunk_overlap: Mapped[int] = mapped_column(nullable=False)
    embedding_model: Mapped[str] = mapped_column(String(100), nullable=False)
    chunks_count: Mapped[int] = mapped_column(nullable=False, default=0)

    user: Mapped["UserDBModel"] = relationship(
        "UserDBModel", back_populates="documents"
    )

    def __repr__(self) -> str:
        return (
            f"<DocumentsDBModel id={self.id} uuid={self.uuid} filename={self.filename}>"
        )
