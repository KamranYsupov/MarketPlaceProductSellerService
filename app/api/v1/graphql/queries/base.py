import strawberry

from . import ProductQuery, SellerQuery


@strawberry.type
class BaseQuery(
    ProductQuery, 
    SellerQuery,
):
    pass
