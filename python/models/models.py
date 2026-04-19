from datetime import datetime
from typing import Optional

from sqlmodel import Column, SQLModel, Field, String, Relationship
from sqlalchemy import func


class Estado(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nombre: str = Field(sa_column=Column(String, nullable=False))

    usuarios: list["Usuario"] = Relationship(back_populates="estado")


class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nombre: str = Field(sa_column=Column(String, nullable=False))

    slug: str = Field(sa_column=Column(String, nullable=False))


# administrador o cliente
class Perfil(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    usuarios: list["Usuario"] = Relationship(back_populates="perfil")

    nombre: str = Field(sa_column=Column(String, nullable=False))


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    estado_id: int | None = Field(default=None, foreign_key="estado.id")
    estado: Optional[Estado] = Relationship(back_populates="usuarios")

    perfil_id: int | None = Field(default=None, foreign_key="perfil.id")
    perfil: Optional[Perfil] = Relationship(back_populates="usuarios")

    nombre: str = Field(sa_column=Column(String, nullable=False))
    correo: str = Field(sa_column=Column(String, nullable=False))
    telefono: str = Field(sa_column=Column(String, nullable=False))
    password: str = Field(sa_column=Column(String, nullable=False))
    token: str = Field(sa_column=Column(String, nullable=False))
    fecha: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={"server_default": func.now()}
    )
