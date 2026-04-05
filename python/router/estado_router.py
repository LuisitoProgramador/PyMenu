from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse

from database import get_session
from sqlmodel import Session, desc, select
from models.models import Estado

from interfaces.interfaces import GenericInterface
from .dto.estado_dto import EstadoDto

router = APIRouter(prefix="/estado", tags=["Estado"])


# obtenemos todos los datos
@router.get("/", response_model=list[Estado])
async def index(session=Depends(get_session)):
    # datos = session.query(Estado).all()
    datos = session.query(Estado).order_by(desc(Estado.id)).all()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[dato.model_dump() for dato in datos],
    )


# obtenemos un dato por id
@router.get("/{id}", response_model=Estado)
async def show(session=Depends(get_session), id: int = 1):
    dato = session.get(Estado, id)

    if not dato:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recurso no disponible",
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=dato.model_dump())


# creamos un nuevo registro
@router.post("/", response_model=GenericInterface)
async def create(dto: EstadoDto, session: Session = Depends(get_session)):
    # Personalizar el nombre antes de guardar
    dto.nombre = f"{dto.nombre} - Creado"
    # Validacion antes de crear el registro
    statement = select(Estado).where(Estado.nombre == dto.nombre)
    existe = session.exec(statement).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrio un error inesperado",
        )

    # Se crea el registro
    try:
        data_db = Estado(**dto.model_dump())
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
    dto: EstadoDto,
    session=Depends(get_session),
    id: int = 1,
):
    dato = session.get(Estado, id)

    if not dato:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recurso no disponible",
        )

    try:
        dato.nombre = dto.nombre
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
    dato = session.get(Estado, id)

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
