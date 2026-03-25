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

## 🚀 Proof - Comportamiento Reactivo

El endpoint `/slow` simula una operación lenta de 3 segundos (como una query a BD o llamada a API externa).

```bash
# Lanzá 5 requests al mismo tiempo
for i in {1..5}; do
  curl https://starfish-app-9doop.ondigitalocean.app/slow &
done
```

**Resultado esperado:** Los 5 responden en ~3s (en paralelo)

**Si fuera síncrono:** 3s, 6s, 9s, 12s, 15s (uno por uno)

Esto demuestra que el event loop maneja múltiples requests simultáneos con un solo thread. ✅

---

## Instalación

### Requisitos
- **Python 3.10+**
- **MongoDB** (local o Atlas)
- **pip** (package manager)

### 1. Clonar proyecto
```bash
git clone https://github.com/TU_USER/reactive-microservice-python.git
cd reactive-microservice-python
```

### 2. Crear virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Setear variable de entorno
```bash
export MONGODB_URL="mongodb+srv://user:password@cluster.mongodb.net/reactive_db?appName=Cluster0"
```

### 5. Correr servidor
```bash
python3 -m uvicorn main:app --reload
```

---

## Endpoints

### 🔥 Reactive Proof
```bash
for i in {1..5}; do
  curl https://starfish-app-9doop.ondigitalocean.app/slow &
done
```

### CRUD Items

```bash
# Crear
curl -X POST https://starfish-app-9doop.ondigitalocean.app/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "Dell XPS", "price": 1500}'

# Listar
curl "https://starfish-app-9doop.ondigitalocean.app/items?skip=0&limit=10"

# Obtener por ID
curl https://starfish-app-9doop.ondigitalocean.app/items/{id}

# Buscar
curl "https://starfish-app-9doop.ondigitalocean.app/search?q=laptop"

# Batch create
curl -X POST https://starfish-app-9doop.ondigitalocean.app/items/batch \
  -H "Content-Type: application/json" \
  -d '[{"name": "Mouse", "price": 50}, {"name": "Teclado", "price": 80}]'

# Actualizar
curl -X PUT https://starfish-app-9doop.ondigitalocean.app/items/{id} \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated", "price": 2000}'

# Eliminar
curl -X DELETE https://starfish-app-9doop.ondigitalocean.app/items/{id}
```

### 📖 Swagger UI
```
https://starfish-app-9doop.ondigitalocean.app/docs
```

---

## Arquitectura
```
FastAPI (async framework)
    ↓
Motor (async MongoDB driver)
    ↓
MongoDB Atlas
```

---

## Stack
```
fastapi
uvicorn
motor
pymongo
pydantic
certifi
```