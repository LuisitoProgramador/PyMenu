from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

# rutas

from router.upload_router import router as upload_router


# inicializamos fastapi
app = FastAPI()

# agregamos las rutas al app

app.include_router(upload_router)


@app.get("/")
def index():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"estado": "oks"})


# manejador de errores para 404
@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def not_found(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"estado": "error", "mensaje": "Recurso no encontrado"},
    )


# para metodos http no usados
@app.exception_handler(StarletteHTTPException)
async def method_not_allowed(request: Request, exc: StarletteHTTPException):
    if exc.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content={"estado": "error", "mensaje": "Metodo no permitido"},
        )
    # si no es un error de metodo no permitido, devolvemos el error original
    return JSONResponse(
        status_code=exc.status_code, content={"estado": "error", "mensaje": exc.detail}
    )


# validaciones dto
@app.exception_handler(RequestValidationError)
async def manejar_errores_validacion(request: Request, exc: RequestValidationError):
    errores_personalizados = []

    for error in exc.errors():
        campo = error["loc"][-1]
        mensaje = error["msg"]

        # Procesar ValueError con ("campo", "mensaje")
        if mensaje.startswith("Value error,"):
            try:
                _, custom_msg = eval(error["input"])
                mensaje = custom_msg
            except:
                pass

        elif mensaje == "Input should be a valid integer":
            mensaje = f"El campo {campo} debe ser un número entero"

        elif mensaje == "Field required":
            mensaje = f"El campo {campo} es obligatorio"

        errores_personalizados.append({"campo": campo, "mensaje": mensaje})

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "estado": "error",
            "mensaje": "Errores de validación",
            "errores": errores_personalizados,
        },
    )
