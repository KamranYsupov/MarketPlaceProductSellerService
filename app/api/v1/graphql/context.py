from typing import Annotated

from strawberry.fastapi import BaseContext
from fastapi import Depends
from dependency_injector.wiring import Provide, inject

from app.core.container import Container

class Context(BaseContext):
    @inject
    def __init__(
        self,
        container: Container = Depends(
            Provide[Container]
        ),
   ): 
       self.container = container

def get_context():
    return Context()

