from datetime import datetime

from sqlalchemy import types, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin(object):
    created_at: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True),
        default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True),
        onupdate=func.now(),
        default=func.now(),
        nullable=False,
    )
