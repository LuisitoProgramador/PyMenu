from pydantic import BaseModel


class GenericInterface(BaseModel):
    estado: str
    mensaje: str
