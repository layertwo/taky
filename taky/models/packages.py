import datetime

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Package(Base):
    __tablename__ = "packages"
    __table_args__ = (UniqueConstraint("hash"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(String(64), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(1024), nullable=False)
    uploader_dn: Mapped[str | None] = mapped_column(String(512), nullable=True)
    upload_ts: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    keywords: Mapped[str | None] = mapped_column(Text, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tool: Mapped[str | None] = mapped_column(String(255), nullable=True)

    def __repr__(self):
        return f"<Package id={self.id} hash={self.hash!r}>"
