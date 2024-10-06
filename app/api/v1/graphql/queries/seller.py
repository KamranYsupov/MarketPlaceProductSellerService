from typing import Annotated, Optional, List
from uuid import UUID

import strawberry
from fastapi import Depends
from strawberry.fastapi import BaseContext, GraphQLRouter
from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.extensions import DependencyExtension
from app.utils.orm import get_orm_statement_by_selected_fields
from app.core.container import Container
from app.services import SellerService
from app.schemas.product import ProductSchema
from app.schemas.seller import SellerProductsSchema
from app.db.models import Seller
from ..types.seller import SellerType


@strawberry.type(extend=True)
class SellerQuery:

    @strawberry.field(extensions=[DependencyExtension()])
    @inject
    async def get_seller(
        self,
        info: strawberry.Info,
        seller_id: str,
        session: AsyncSession = Provide[Container.session],
        seller_service: SellerService = Provide[Container.seller_service],
    ) -> SellerType:
        statement = get_orm_statement_by_selected_fields(
            model=Seller,
            info=info
        ).filter_by(id=UUID(seller_id))
        result = await session.execute(statement)
        
        seller = result.scalars().first()
        seller_data = seller.serialize(schema_class=SellerProductsSchema) 
          
        return SellerType.from_data(seller_data)

     
