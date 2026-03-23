# Reactive Microservice - Python

POC de microservicio reactivo con **FastAPI** y **MongoDB** (equivalente a Spring Boot Reactive).

## ¿Qué es Reactive Programming?

Reactive programming maneja múltiples requests sin bloquear threads.

**Comparación:**

| Métrica | Síncrono | Reactivo |
|:--------|:----------:|:----------:|
| **Threads por request** | 1 thread | Compartido (event loop) |
| **100 requests simultáneos** | 100 threads 🔴 | 1 thread ✅ |
| **Uso de memoria** | Alto | Bajo |
| **Tiempo total** | 100 requests = 100s | 100 requests = ~1s |

---

## Instalación

### Requisitos
- **Python 3.10+**
- **MongoDB** (local o Docker)
- **pip** (package manager)

### 1. Clonar proyecto
```bash
git clone https://github.com/TU_USER/reactive-microservice-python.git
cd reactive-microservice-python
```

### 2. Crear virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
python3 -m pip install -r requirements.txt
```

### 4. Iniciar MongoDB
```bash
# Opción A: Docker (recomendado)
docker run -d -p 27017:27017 mongo

# Opción B: Local (si tienes MongoDB instalado)
mongod
```

### 5. Correr servidor
```bash
python3 -m uvicorn main:app --reload
```

Deberías ver:
```
Uvicorn running on http://127.0.0.1:8000
```

---

## Usar la API

### Swagger UI (interactivo)
Abre en tu browser: **http://localhost:8000/docs**

### Ejemplos con curl

**1. GET root**
```bash
curl http://localhost:8000/
```

**2. Crear item (POST)**
```bash
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "Dell XPS", "price": 1500}'
```

Response:
```json
{"id": "507f1f77bcf86cd799439011", "created": true}
```

**3. Buscar (GET con query)**
```bash
curl "http://localhost:8000/search?q=laptop&limit=5"
```

**4. Obtener por ID (GET con path)**
```bash
curl http://localhost:8000/items/507f1f77bcf86cd799439011
```

**5. Listar items (GET)**
```bash
curl "http://localhost:8000/items?skip=0&limit=10"
```

**6. Actualizar (PUT)**
```bash
curl -X PUT http://localhost:8000/items/507f1f77bcf86cd799439011 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated", "price": 2000}'
```

**7. Eliminar (DELETE)**
```bash
curl -X DELETE http://localhost:8000/items/507f1f77bcf86cd799439011
```

---

## Arquitectura
```
FastAPI (async framework)
    ↓
Motor (async MongoDB driver)
    ↓
MongoDB
```

**¿Por qué async?**
- `async def` = no bloquea el thread
- `await` = espera sin bloquear
- Event loop maneja múltiples requests

---

## Archivo de dependencias

El `requirements.txt` tiene:
```
fastapi==0.104.1
uvicorn==0.24.0
motor==3.3.2
pymongo==4.6.0
pydantic==2.5.0
```

---

## Próximos pasos

- [ ] Validaciones y manejo de errores
- [ ] Logging
- [ ] Dockerfile
- [ ] Tests
- [ ] Autenticación JWT

---

**Info extra:** Reactive = No bloqueas threads, usas async/await para que un único thread maneje múltiples requests simultáneamente.
