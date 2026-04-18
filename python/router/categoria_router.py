from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from slugify import slugify

from database import get_session
from sqlmodel import Session, desc, select
from models.models import Categoria

from interfaces.interfaces import GenericInterface
from .dto.categoria_dto import CategoriaDto
from models.models import Categoria

router = APIRouter(prefix="/categoria", tags=["Categoria"])


@router.get("/", response_model=list[Categoria])
async def index(session: Session = Depends(get_session)):
    datos = session.query(Categoria).order_by(desc(Categoria.id)).all()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[dato.model_dump() for dato in datos],
    )


@router.get("/{id}", response_model=Categoria)
async def show(id: int, session: Session = Depends(get_session)):
    dato = session.get(Categoria, id)
    if not dato:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recurso no disponible",
        )
    return dato


# creamos un nuevo registro
@router.post("/", response_model=GenericInterface)
async def create(dto: CategoriaDto, session: Session = Depends(get_session)):

    # Validacion antes de crear el registro
    statement = select(Categoria).where(Categoria.nombre == dto.nombre)
    existe = session.exec(statement).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrio un error inesperado",
        )
    # creamos un objeto de Categoria pasando tambien el slug
    data_db = Categoria(nombre=dto.nombre, slug=slugify(dto.nombre))
    # Se crea el registro
    try:
        session.add(data_db)
        session.commit()
        session.refresh(data_db)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"estado": "ok", "mensaje": "Se crea el registro exitosamente"},
        )

    except:
        session.rollback()  # Revierte cualquier cambio pendiente
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado",
        )


# actualizamos un registro por id
@router.put("/{id}", response_model=GenericInterface)
async def update(
    dto: CategoriaDto,
    session=Depends(get_session),
    id: int = 1,
):
    dato = session.get(Categoria, id)

    if not dato:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recurso no disponible",
        )

    try:
        dato.nombre = dto.nombre
        dato.slug = slugify(dto.nombre)

        session.commit()
        session.refresh(dato)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "estado": "ok",
                "mensaje": "Se actualiza el registro exitosamente",
            },
        )

    except Exception as e:
        session.rollback()  # Revierte cualquier cambio pendiente
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado",
        )


# eliminamos un registro por id
@router.delete("/{id}", response_model=GenericInterface)
async def delete(
    session=Depends(get_session),
    id: int = 1,
):
    dato = session.get(Categoria, id)

    if not dato:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recurso no disponible",
        )

    try:
        session.delete(dato)
        session.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "estado": "ok",
                "mensaje": "Se elimina el registro exitosamente",
            },
        )

    except Exception as e:
        session.rollback()  # Revierte cualquier cambio pendiente
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado",
        )
