from typing import List, Tuple

from .mixins import CRUDServiceMixin
from app.repositories.seller import RepositorySeller


class SellerService(CRUDServiceMixin):
    def __init__(
        self, 
        repository_seller: RepositorySeller,
        unique_fields: List[str] | Tuple[str] | None = None,
    ):
        self._repository_seller = repository_seller
        super().__init__(
            repository=repository_seller, 
            unique_fields=unique_fields,
        )
    