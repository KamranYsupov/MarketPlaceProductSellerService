from typing import TYPE_CHECKING, List

import strawberry

from app.schemas.seller import SellerSchema
from .base import BaseSellerType, BaseProductType


@strawberry.type(name='Seller')
class SellerType(BaseSellerType):
    products: List[BaseProductType]

  