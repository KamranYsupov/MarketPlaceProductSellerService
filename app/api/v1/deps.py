from uuid import UUID

import aiohttp
from dependency_injector.wiring import inject, Provide
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.core.container import Container
from app.services import SellerService
from app.db.models import Seller
from app.utils.http import get_response_data_or_raise_http_exception

http_bearer = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{settings.auth_users_service_api_v1_url}/users/me/',
            headers={'Authorization': f'Bearer {token}'}
        ) as response:
            return await get_response_data_or_raise_http_exception(response)
            
@inject
async def get_current_seller(
    user: dict = Depends(get_current_user),
    seller_service: SellerService = Depends(
          Provide[Container.seller_service]
     ),
) -> Seller:
     seller = await seller_service.get(user_id=UUID(user['id']))
      
     if not seller:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Current user is not seller'
         )
     return seller
