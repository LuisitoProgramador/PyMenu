FROM node:21

 

WORKDIR /app




# Copiar package.json y package-lock.json si existen (para futuras instalaciones)
#COPY package*.json ./
COPY . ./

# Exponer el puerto que usará la aplicación
EXPOSE 5173

# Comando por defecto (mantiene el contenedor corriendo)
CMD ["tail", "-f", "/dev/null"]