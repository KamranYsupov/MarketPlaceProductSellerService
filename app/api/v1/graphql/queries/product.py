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
from app.services import ProductService
from app.schemas.product import ProductSchema
from app.db.models import Product
from ..types.product import ProductType


@strawberry.type(extend=True)
class ProductQuery:

    @strawberry.field(extensions=[DependencyExtension()])
    @inject
    async def get_products(
        self,
        info: strawberry.Info,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        session: AsyncSession = Provide[Container.session],
        product_service: ProductService = Provide[Container.product_service],
    ) -> List[ProductType]:
        statement = get_orm_statement_by_selected_fields(
            model=Product,
            info=info
        ).offset(skip).limit(limit) 
        result = await session.execute(statement)

        products_data = [
            product.serialize(schema_class=ProductSchema)
            for product in result.scalars().all()
        ]

        return [ProductType.from_data(product_dict) for product_dict in products_data]
    
    @strawberry.field(extensions=[DependencyExtension()])
    @inject
    async def get_product(
        self,
        info: strawberry.Info,
        product_id: str,
        session: AsyncSession = Provide[Container.session],
        product_service: ProductService = Provide[Container.product_service],
    ) -> ProductType:
        statement = get_orm_statement_by_selected_fields(
            model=Product, 
            info=info
        ).filter_by(id=UUID(product_id))
        result = await session.execute(statement)

        product = result.scalars().first()
        product_data = product.serialize(schema_class=ProductSchema)

        return ProductType.from_data(product_data)
    
    @strawberry.field(extensions=[DependencyExtension()])
    @inject
    async def get_products_by_ids(
        self,
        info: strawberry.Info,
        ids: List[str],
        session: AsyncSession = Provide[Container.session],
        product_service: ProductService = Provide[Container.product_service],
    ) -> List[ProductType]:
        uuids = [UUID(product_id) for product_id in ids]
        statement = get_orm_statement_by_selected_fields(
            model=Product,
            info=info
        ).filter(Product.id.in_(uuids))
        result = await session.execute(statement)

        products_data = [
            product.serialize(schema_class=ProductSchema)
            for product in result.scalars().all()
        ]

        return [ProductType.from_data(product_dict) for product_dict in products_data]
    
