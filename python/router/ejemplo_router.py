from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from .dto.ejemplo_dto import EjemploDTO

router = APIRouter(prefix="/ejemplo", tags=["ejemplo"])

@router.get("/")
async def index():
    return JSONResponse(content={"message": "Metedo GET"}, status_code=status.HTTP_200_OK) 

@router.get("/{id}")
async def get_by_id(id: int):
    return JSONResponse(content={"message": f"Metedo GET con id {id}"}, status_code=status.HTTP_200_OK)


@router.post("/")
async def create(dto: EjemploDTO):
    return JSONResponse(content={"message": f"Metedo POST con datos: {dto.nombre}, {dto.description}, {dto.precio}, {dto.disponible}"}, status_code=status.HTTP_201_CREATED)

@router.put("/")
async def update():
    return JSONResponse(content={"message": "Metedo PUT"}, status_code=status.HTTP_200_OK)

@router.delete("/")
async def delete():
    return JSONResponse(content={"message": "Metedo DELETE"}, status_code=status.HTTP_200_OK)
 
  