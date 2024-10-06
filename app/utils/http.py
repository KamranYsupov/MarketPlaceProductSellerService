import aiohttp
from aiohttp.client_reqrep import ClientResponse
from fastapi import HTTPException


async def get_response_data_or_raise_http_exception(
    response: ClientResponse
):
    response_data = await response.json()
    if response.status == 200:
        return response_data
            
    raise HTTPException(
        detail=response_data['detail'],
        status_code=response.status
    )