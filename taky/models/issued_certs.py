import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class IssuedCert(Base):
    __tablename__ = "issued_certs"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String(512), nullable=False)
    serial: Mapped[str] = mapped_column(String(64), nullable=False)
    expiry: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    issuer: Mapped[str] = mapped_column(String(512), nullable=False)

    def __repr__(self):
        return f"<IssuedCert id={self.id} serial={self.serial!r}>"
