# Imagen base
FROM python:3.12-slim

# Directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY main.py .

# Exponer puerto
EXPOSE 8000

# Comando para correr
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
