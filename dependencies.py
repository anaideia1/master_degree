from typing import Annotated
from fastapi import Depends

from repositories.unitofwork import IUnitOfWork, UnitOfWork


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
