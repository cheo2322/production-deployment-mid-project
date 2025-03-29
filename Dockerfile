# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar todos los archivos al contenedor
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar el modelo para generar los archivos necesarios
RUN python /models/3_knn_users_based.py

# Exponer el puerto para Flask
EXPOSE 5000

# Comando para ejecutar la app Flask
CMD ["python", "/app/app.py"]