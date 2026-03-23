# Reactive Programming - Conceptos

## ¿Qué es Reactive Programming?

Reactive programming es un paradigma que maneja **streams de datos asincronos**. En lugar de esperar a que una operación termine, tu código reacciona cuando los datos están listos.

---

## En Java vs Python

### Spring Boot Reactive (Java)
```java
@GetMapping("/items/{id}")
public Mono<Item> getItem(@PathVariable String id) {
    return itemRepository.findById(id)
        .subscribeOn(Schedulers.boundedElastic());
}
```

Usa `Mono<T>` (0 o 1 elemento) y `Flux<T>` (múltiples elementos) de Project Reactor.

### FastAPI Reactive (Python)
```python
@app.get("/items/{id}")
async def get_item(id: str):
    item = await db.items.find_one({"_id": ObjectId(id)})
    return item
```

Usa `async/await` que es lo equivalente.

---

## ¿Cómo Funciona?

### Conceptos clave:
1. **async** = la función no bloquea el thread
2. **await** = espera el resultado sin bloquear
3. **Event loop** = maneja múltiples requests en paralelo

---

## Ejemplo: Sin async (BLOQUEA)
```python
def get_user(user_id):
    result = db.users.find_one({"_id": user_id})  # ⏸️ ESPERA aquí
    return result

# Simulación:
# Request 1: Tarda 1s (bloquea thread)
# Request 2: Espera a que termine Request 1, luego tarda 1s
# Request 3: Espera a que terminen 1 y 2, luego tarda 1s
# Total: 3 segundos con 3 threads
```

---

## Ejemplo: Con async (NO BLOQUEA)
```python
async def get_user(user_id):
    result = await db.users.find_one({"_id": user_id})  # ⚡ NO espera
    return result

# Simulación:
# Request 1: Inicia, va al DB, mientras espera...
# Request 2: Inicia, va al DB, mientras espera...
# Request 3: Inicia, va al DB, mientras espera...
# Todos esperan "en paralelo" = ~1 segundo total con 1 thread
```

---

## Visualización

### Síncrono (cada request usa 1 thread):
```
Thread 1: [████████] 1s
Thread 2: [████████] 1s
Thread 3: [████████] 1s
─────────────────────
Total: 3 segundos
```

### Reactivo (1 event loop):
```
Thread 1: [████] [████] [████] (alterna entre requests)
─────────────────────
Total: ~1 segundo
```

---

## Ventajas Reactive

| Aspecto | Síncrono | Reactivo |
|:--------|:----------:|:----------:|
| **Threads por request** | 1 | Compartido |
| **100 requests** | 100 threads | 1 thread |
| **Memoria por thread** | ~1MB | ~1KB (event loop) |
| **Tiempo total** | 100s | ~1s |
| **CPU** | Alto (context switching) | Bajo |
| **Escalabilidad** | Limitada | Excelente |

---

## El Event Loop

Python tiene un **event loop** que dice:
```
1. ¿Hay requests? Sí → Ejecuta
2. ¿Espera a BD? Sí → Cambia a otro request
3. ¿BD respondió? Sí → Continúa ese request
4. Repite
```

Todo en **1 thread**, sin bloqueos.

---

## Diferencia: Blocking vs Non-Blocking

### Blocking (Síncrono):
```python
# Espera a que MongoDB responda
result = db.find_one({"_id": 1})  # ⏸️ Bloquea aquí
print(result)
```

### Non-Blocking (Reactivo):
```python
# No espera, sigue adelante
result = await db.find_one({"_id": 1})  # ⚡ No bloquea
print(result)
```

---

## Cuándo usar Reactive

✅ **Usa reactive si:**
- Tienes muchos I/O operations (DB, APIs externas)
- Necesitas manejar miles de requests simultáneos
- Bajas en memoria son críticas
- Tienes operaciones que esperan (REST calls, queries)

❌ **No uses reactive si:**
- CPU-bound (cálculos pesados)
- Lógica simple sin I/O
- Equipo no está familiarizado con async

---

## Drivers async en Python

Para que reactive funcione, **necesitas drivers async**:

| BD | Driver Sync | Driver Async |
|:---|:-----------|:------------|
| MongoDB | `pymongo` | `motor` |
| PostgreSQL | `psycopg2` | `asyncpg` |
| MySQL | `mysql-connector` | `aiomysql` |
| Redis | `redis-py` | `aioredis` |

**Importante:** `motor` es `pymongo` + async. Sin él, sigue siendo blocking.

---

## FastAPI + Motor = Reactive
```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.reactive_db

@app.get("/items/{id}")
async def get_item(id: str):
    # Motor maneja el async automáticamente
    item = await db.items.find_one({"_id": ObjectId(id)})
    return item
```

**Flujo:**
1. FastAPI recibe GET request
2. `await db.items...` no bloquea
3. Event loop puede manejar otros requests
4. MongoDB responde → continúa

---

## Cheat Sheet
```python
# ❌ Síncrono (bloquea)
def get_data():
    return db.find()

# ✅ Reactivo (no bloquea)
async def get_data():
    return await db.find()
```
```python
# ❌ Endpoint síncrono
@app.get("/data")
def get_data():
    return db.find()

# ✅ Endpoint reactivo
@app.get("/data")
async def get_data():
    return await db.find()
```

---

## Resumen

**Reactive = async/await + drivers async + event loop = múltiples requests sin bloquear threads.**

