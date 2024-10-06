from typing import Dict, List

from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

from app.core.container import Container
from app.db.models import Seller
from app.schemas.product import CreateProductSchema, UpdateProductSchema, ProductSchema
from app.schemas.seller import SellerSchema
from app.services import ProductService, SellerService
from ..deps import get_current_user, get_current_seller

router = APIRouter(tags=['Product'], prefix='/products')


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ProductSchema,
)
@inject
async def create_product(
    create_product_schema: CreateProductSchema,
    seller: Seller = Depends(get_current_seller),
    product_service: ProductService = Depends(Provide[Container.product_service]),
) -> ProductSchema:
    create_product_schema.seller_id = seller.id
    product = await product_service.create(obj_in=create_product_schema)
    seller_schema = SellerSchema(
        id=seller.id,
        name=seller.name,
        bio=seller.bio,
        is_verified=seller.is_verified,
    )
    product_schema = ProductSchema(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        rating=product.rating,
        quantity=product.quantity,
        seller=seller_schema
    )
    return product_schema



@router.put(
    '/update',
    status_code=status.HTTP_200_OK,
    response_model=List[ProductSchema],
)
@inject
async def update_products(
    update_product_schemas: List[UpdateProductSchema],
    user: dict = Depends(get_current_user),
    product_service: ProductService = Depends(Provide[Container.product_service]),
) -> List[ProductSchema]:
    await product_service.bulk_update(update_product_schemas)
    
    product_ids = [product_schema.id for product_schema in update_product_schemas]
    products = await product_service.get_products_by_ids(ids=product_ids)
 
    product_schemas = [
        product.serialize(
            schema_class=ProductSchema,
            model_dump=False, 
            exclude_fields=('seller', )
        ) for product in products
    ]

    return product_schemas 





