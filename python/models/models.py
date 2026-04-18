from sqlmodel import Column, SQLModel, Field, String


class Estado(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(sa_column=Column(String, nullable=False))


class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(sa_column=Column(String, nullable=False))
    slug: str = Field(sa_column=Column(String, nullable=False))
