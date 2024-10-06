from dependency_injector import containers, providers

from app.repositories import (
    RepositoryProduct, 
    RepositorySeller,
)
from app.services import (
    ProductService,
    SellerService,
)
from app.db import DataBaseManager
from app.db.models import (
    Product,
    Seller,
)
from app.core.config import settings




class Container(containers.DeclarativeContainer):
    db_manager = providers.Singleton(DataBaseManager, db_url=settings.db_url)
    session = providers.Resource(db_manager().get_async_session)

    # region repository
    repository_product = providers.Singleton(
        RepositoryProduct, model=Product, session=session
    )
    repository_seller = providers.Singleton(
        RepositorySeller, model=Seller, session=session
    )
    # endregion

    # region services
    product_service = providers.Singleton(
        ProductService,
        repository_product=repository_product,
    )
    seller_service = providers.Singleton(
        SellerService, 
        repository_seller=repository_seller,
        unique_fields=('name', 'user_id'),
    )
    # endregion


container = Container()
container.init_resources()
container.wire(modules=settings.container_wiring_modules)
