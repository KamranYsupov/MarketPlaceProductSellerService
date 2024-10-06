from uuid import UUID
from typing import Dict, Any

from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status

from app.core.container import Container
from app.schemas.seller import CreateSellerSchema, SellerSchema
from app.services.seller import SellerService
from ..deps import get_current_user

router = APIRouter(tags=['Seller'], prefix='/seller')

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=SellerSchema,
)
@inject
async def create_seller(
    create_seller_schema: CreateSellerSchema,
    user: dict = Depends(get_current_user),
    seller_service: SellerService = Depends(Provide[Container.seller_service]),
) -> SellerSchema:
    create_seller_schema.user_id = UUID(user['id'])
    seller = await seller_service.create(obj_in=create_seller_schema)
    seller_schema = SellerSchema(
        id=seller.id,
        name=seller.name,
        bio=seller.bio,
        is_verified=seller.is_verified,
    )
    return seller_schema
