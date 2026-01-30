import uuid as uuid_pkg
from datetime import datetime  # noqa

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import DateTime, UUID, func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, default=uuid_pkg.uuid4, nullable=False
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class AutoincrementIDMixin:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)


class Base(DeclarativeBase):
    metadata: MetaData = MetaData()
