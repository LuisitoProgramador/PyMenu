from fastapi import APIRouter, status, Form, UploadFile, Query
from fastapi.responses import FileResponse, JSONResponse
from typing import Annotated
import uuid
import os
import boto3

# dotenv
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/upload", tags=["upload"])


# Cliente s3 apuntando a localstack
s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    endpoint_url=os.getenv("AWS_SECRET_ACCESS_URL"),
)
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


# Subir un archivo a s3
@router.post("/")
async def upload_file(negocio_id: Annotated[int, Form()], file: UploadFile):
    extension = "0"
    if file.content_type == "image/jpeg":
        extension = "jpg"
    if file.content_type == "image/png":
        extension = "png"
    if extension == "0":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"estado": "error", "mensaje": f"Ocurrio un error inesperado."},
        )

    # generar un nombre unico
    nombre = f"{uuid.uuid4()}.{extension}"
    # guardar el archivo en s3
    try:
        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            f"archivos/{nombre}",
            ExtraArgs={"ContentType": file.content_type},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "estado": "error",
                "mensaje": f"Ocurrio un error inesperado: {str(e)}",
            },
        )
    file_url = f"http://localhost:8000/{S3_BUCKET_NAME}/archivos/{nombre}"
    # devolver la respuesta
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "estado": "ok",
            "mensaje": f"Archivo subido correctamente para el negocio con id: {negocio_id}, nombre del archivo: {file.filename}, tipo de archivo: {file.content_type}, tamaño del archivo: {file.size} bytes, mimetype del archivo: {file.content_type}, nombre unico generado: {nombre}",
            "url": file_url,
        },
    )


# Eliminar un archivo de s3
@router.delete("/file")
async def eliminar_archivo(
    file_name: str = Query(..., description="ID del archivo a eliminar")
):

    # Verificar si el archivo existe antes de intentar eliminarlo
    try:
        s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=f"archivos/{file_name}")
    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "estado": "error",
                    "mensaje": f"Ocurrio un error inesperado.",
                },
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "estado": "error",
                    "mensaje": f"Ocurrio un error inesperado.",
                },
            )

    # Eliminar el archivo de S3
    try:
        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=f"archivos/{file_name}")
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "estado": "error",
                "mensaje": f"Ocurrio un error inesperado: {str(e)}",
            },
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "estado": "ok",
            "mensaje": f"Archivo eliminado correctamente: {file_name}",
        },
    )


# Renderizacion archivo con FileResponse y querystring
@router.get("/file")
async def ejemplo_foto(id: str = Query(..., description="ID del archivo a renderizar")):
    if not os.path.exists(f"uploads/{id}"):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"estado": "error", "mensaje": f"Ocurrio un error inesperado."},
        )
    return FileResponse(f"uploads/{id}")


"""
# Validar el tipo de archivo con mimetype
@router.post("/")
async def upload_file(negocio_id: Annotated[int, Form()], file: UploadFile):
    extension = "0"
    if file.content_type == "image/jpeg":
        extension = "jpg"
    if file.content_type == "image/png":
        extension = "png"
    if extension == "0":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"estado": "error", "mensaje": f"Ocurrio un error inesperado."},
        )

    # generar un nombre unico
    nombre = f"{uuid.uuid4()}.{extension}"
    # guardar el archivo en el servidor
    file_location = os.path.join("uploads", nombre)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    # devolver la respuesta
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "estado": "ok",
            "mensaje": f"Archivo subido correctamente para el negocio con id: {negocio_id}, nombre del archivo: {file.filename}, tipo de archivo: {file.content_type}, tamaño del archivo: {file.size} bytes, mimetype del archivo: {file.content_type}, nombre unico generado: {nombre}",
        },
    )

#Recibir valor formdata y de tipo file
@router.post("/")
async def upload_file(negocio_id: Annotated[int, Form()], file: UploadFile):
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content={
            "estado": "ok",
            "mensaje": f"Archivo subido correctamente para el negocio con id: {negocio_id}, nombre del archivo: {file.filename}, tipo de archivo: {file.content_type}, tamaño del archivo: {file.size} bytes, mimetype del archivo: {file.content_type}"
        }
    )
"""
