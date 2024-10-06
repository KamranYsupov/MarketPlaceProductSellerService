import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field


if TYPE_CHECKING:
    from .seller import SellerSchema


class ProductBaseSchema(BaseModel):
    name: str = Field(title='Название продукта')
    description: str = Field(title='Описание')
    price: float = Field(title='Цена', gt=0.0)
    rating: float = Field(title='Оценка', le=5.0, gt=1.0)
    quantity: int = Field(ge=0)
    

class ProductSchema(ProductBaseSchema):
    seller: Optional['SellerSchema'] = Field(title='Продавец', default=None)
    id: uuid.UUID
    
    
class CreateProductSchema(ProductBaseSchema):
    seller_id: Optional[uuid.UUID] = Field(title='ID продавца', default=None)
  

class UpdateProductSchema(ProductBaseSchema):
    id: uuid.UUID

    