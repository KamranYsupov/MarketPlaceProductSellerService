import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field


if not TYPE_CHECKING:
    from .product import ProductSchema


class SellerBaseSchema(BaseModel):
    name: str = Field(title='Имя продавца', max_length=32)
    bio: str | None = Field(title='Информация о продавце', default=None)
    is_verified: bool = Field(title='Подтверждён', default=False)
    

class SellerSchema(SellerBaseSchema):
    id: uuid.UUID
                   

class SellerProductsSchema(SellerSchema):
    products: list['ProductSchema'] 
    
                       
class CreateSellerSchema(SellerBaseSchema):
    user_id: Optional[uuid.UUID] = Field(default=None)