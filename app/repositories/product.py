from uuid import UUID
from typing import List, Dict, Type

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Product
from .base import RepositoryBase, ModelType


class RepositoryProduct(RepositoryBase[Product]):
    """Репозиторий для работы с таблицей products"""
    
    def __init__(
        self, 
        model: Type[ModelType],
        session: AsyncSession
    ):
        self._session = session
        super().__init__(
            model=Product,
            session=session,
        )
        
    async def get_products_by_ids(self, ids: List[UUID]) -> List[Product]:
        statement = select(Product).filter(Product.id.in_(ids))
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def bulk_update(
        self, 
        update_data: List[dict],
    ):
        statement = update(Product)
            
        result = await self._session.execute(
            statement, update_data
        )
        await self._commit_or_rollback()