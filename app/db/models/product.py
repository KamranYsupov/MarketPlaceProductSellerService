from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import Base, TimestampedMixin


if TYPE_CHECKING:
    from .seller import Seller


class Product(Base, TimestampedMixin):
    """Модель товара"""

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    rating: Mapped[float] = mapped_column(default=0)
    quantity: Mapped[int] = mapped_column(default=0)
    seller_id: Mapped[UUID] = mapped_column(
        ForeignKey('sellers.id', ondelete='CASCADE'),
    )

    seller: Mapped['Seller'] = relationship(
        back_populates='products',
        lazy='joined',
    )

