from uuid import UUID

from typing import List, Sequence, Optional

from .mixins import CRUDServiceMixin
from app.repositories import RepositoryProduct
from app.schemas.product import UpdateProductSchema
from app.db.models import Product

class ProductService(CRUDServiceMixin):
    def __init__(
        self, 
        repository_product: RepositoryProduct,
        unique_fields: Optional[Sequence[str]] = None,
    ):
        self._repository_product = repository_product
        super().__init__(
            repository=repository_product,
            unique_fields=unique_fields,
        )

    async def get_products_by_ids(self, ids: List[UUID]) -> List[Product]:
        return await self._repository_product.get_products_by_ids(ids=ids)

    async def bulk_update(
        self, 
        update_schemas: List[UpdateProductSchema],
    ) -> List[Product]:
        update_data = [schema.model_dump() for schema in update_schemas]
        return await self._repository_product.bulk_update(update_data) 
           

    