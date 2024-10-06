from typing import TYPE_CHECKING

import strawberry

from app.schemas.product import ProductSchema
from .base import BaseProductType
from .seller import SellerType


@strawberry.type(name='Product')
class ProductType(BaseProductType):
    seller: SellerType 

    
       

