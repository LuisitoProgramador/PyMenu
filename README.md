# udemy_fast_api_mvp
# docker compose down && docker system prune --all && docker volume prune --all
## docker exect -it python service unicorn main::app --host 0.0.0.0 --port 8050 --reload

# Código para creación bucket en localstack
#entrar al contenedor

docker exec -it localstack bash

# crear bucket

docker exec -it localstack awslocal s3 mb s3://curso-udemy

# listar bucket

docker exec -it localstack awslocal s3 ls

# Listar objetos en el bucket "mi-bucket"

docker exec -it localstack awslocal s3 ls s3://curso-udemy/

# Listar recursivamente (todos los archivos y subcarpetas)

docker exec -it localstack awslocal s3 ls s3://curso-udemy/ --recursive

# borrar bucket

docker exec -it localstack awslocal s3 rb s3://curso-udemy2 --force

# alembic
docker exec -it python_service alembic init alembic
docker exec -it python_service alembic revision --autogenerate -m "Tabla estado"
docker exec -it python_service alembic upgrade head

