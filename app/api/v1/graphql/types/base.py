import strawberry


@strawberry.type(extend=True)
class BaseType:
    """Базовый Type"""
    id: str

    @classmethod
    def from_data(cls, data: dict):
        return cls(**data)


@strawberry.type(extend=True)
class BaseProductType(BaseType):
    """Базовый тип товара"""
    name: str
    description: str
    price: float
    rating: float
    quantity: int


@strawberry.type(extend=True)
class BaseSellerType(BaseType):
    """Базовый тип продавца"""
    name: str
    bio: str
    is_verified: bool
