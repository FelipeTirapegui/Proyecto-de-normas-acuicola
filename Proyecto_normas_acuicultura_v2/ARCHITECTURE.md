# 🏗️ Architecture - Motor de Normativas v2.0

Descripción técnica de la arquitectura del sistema.

---

## **Diagram Alto Nivel**

```
┌─────────────────────────────────────────────────────────────┐
│                    NAVEGADOR (Frontend)                     │
│                     index.html + JS                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • Interfaz de búsqueda                               │  │
│  │ • Modal corpus                                       │  │
│  │ • Filtros (mercado, categoría)                      │  │
│  │ • Visualización de resultados                       │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬──────────────────────────────────────────────┬─┘
             │ HTTP POST/GET                                │
             │ JSON                                         │
             │ (CORS enabled)                               │
             ▼                                              ▼
┌──────────────────────────────┐  ┌──────────────────────────────┐
│   FASTAPI BACKEND            │  │   ARCHIVOS ESTÁTICOS         │
│   http://127.0.0.1:8000      │  │                              │
│ ┌──────────────────────────┐ │  │ • embeddings.npy (43x384)    │
│ │ Endpoints:               │ │  │ • embeddings_indice.json     │
│ │ • POST /search           │ │  │ • corpus_stats.json          │
│ │ • GET /corpus            │ │  │                              │
│ │ • POST /gap-analysis     │ │  │ (Pre-computados)             │
│ │ • GET /health            │ │  │                              │
│ └──────────────────────────┘ │  └──────────────────────────────┘
│ ┌──────────────────────────┐ │
│ │ Pipeline:                │ │
│ │ 1. Validar input         │ │
│ │ 2. Vectorizar query      │ │
│ │ 3. Similitud coseno      │ │
│ │ 4. Top-K + threshold     │ │
│ │ 5. Retornar JSON         │ │
│ └──────────────────────────┘ │
└──────────────────────────────┘
```

---

## **CAPAS**

### **Capa 1: Frontend (HTML/JS)**

**Responsabilidad:** Interfaz de usuario

**Archivos:**
- `index.html` (única página, todo en 1 archivo)

**Componentes:**
1. **Input de búsqueda** - Campo de texto + botón
2. **Filtros** - Mercado, categoría
3. **Resultados** - Tabla con normativas
4. **Modal corpus** - Lista completa de 43 normas
5. **Gap analysis** - Comparador multi-mercado

**Tecnologías:**
- Vanilla JavaScript (sin frameworks)
- Fetch API para llamadas HTTP
- CSS Grid/Flexbox
- LocalStorage (para caché opcional)

---

### **Capa 2: Backend (FastAPI)**

**Responsabilidad:** Lógica de negocio + búsqueda semántica

**Archivo:** `main.py`

**Estructura:**

```python
# 1. Cargar datos
CORPUS = [43 normativas con metadata]
embeddings = np.load('embeddings.npy')  # 43x384

# 2. Cargar modelo
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# 3. Endpoints
@app.post("/search")
  → validate query
  → encode query
  → compute similarity
  → filter + sort
  → return top-k

@app.get("/corpus")
  → aggregate metadata
  → return corpus info

@app.post("/gap-analysis")
  → search en mercado A
  → search en mercado B
  → compare results
  → identify gaps

@app.get("/health")
  → return status
```

---

### **Capa 3: Data (Embeddings & Corpus)**

**Responsabilidad:** Datos pre-computados

**Archivos:**

| Archivo | Tamaño | Contenido |
|---------|--------|----------|
| `embeddings.npy` | ~13MB | 43 vectores 384D |
| `embeddings_indice.json` | ~5KB | Mapeo: norma → índice |
| `corpus_stats.json` | ~10KB | Metadata por norma |

**Por qué pre-computados?**
- ⚡ Carga instant (sin delay de encoding)
- 🔒 Determinístico (mismos resultados)
- 💰 Sin API calls (self-contained)
- 🚀 Production-ready

---

## **FLUJO DE DATOS: Search**

```
1. USUARIO ESCRIBE
   Input: "residuos pesticidas"
   
2. FRONTEND VALIDA
   • No vacío
   • Max 500 caracteres
   
3. HTTP POST /search
   {
     "query": "residuos pesticidas",
     "top_k": 5,
     "threshold": 0.3
   }
   
4. BACKEND PROCESA
   a) Vectoriza: "residuos pesticidas" → [384D embedding]
   b) Computa similitud con 43 embeddings almacenados
   c) Selecciona top-5 con score > 0.3
   d) Añade metadata (país, categoría, extracto)
   
5. RETORNA JSON
   {
     "resultados": [
       {
         "norma": "Japón - Food Sanitation...",
         "similitud": 0.87,
         "mercado": "Japón",
         "extracto": "...",
         "keywords": [...]
       },
       ...
     ],
     "tiempo_ms": 145
   }
   
6. FRONTEND RENDERIZA
   • Tabla con resultados
   • Scores visuales (barras)
   • Enlaces a fuentes
```

---

## **MODELO DE EMBEDDINGS**

**Modelo:** `paraphrase-multilingual-mpnet-base-v2`

**Características:**
- 📦 Tamaño: 384 dimensiones
- 🌍 Multilingüe: Español, Inglés, Japonés
- 💪 Entrenado en 50M frases
- ⚡ Inferencia rápida (~100ms / 43 vectores)

**¿Por qué este modelo?**
- ✓ Entiende semántica regulatoria
- ✓ Maneja 4 idiomas nativamente
- ✓ Buena relación tamaño/performance
- ✓ Open source + sin costo

---

## **ALGORITMO: Similitud Coseno**

```python
# Para cada query:
query_embedding = model.encode(query)  # 384D

# Similitud con cada norma:
for i in range(43):
    norma_embedding = embeddings[i]  # 384D
    
    similarity = cosine_similarity(
        query_embedding, 
        norma_embedding
    )  # 0-1
    
    if similarity > threshold:
        results.append((i, similarity))

results.sort(key=score, reverse=True)
return results[:top_k]
```

**Complejidad:**
- Tiempo: O(43) = ~10ms
- Espacio: O(43 × 384) = ~13MB

---

## **ESTRUCTURA DE CORPUS (CORPUS_DATA)**

```python
CORPUS = [
  {
    "id": "c1_1",
    "norma": "USA - 21 CFR Part 123",
    "mercado": "USA",
    "categoria": "SST",
    "año": 1995,
    "descripcion": "...",
    "extracto": "Establece HACCP obligatorio...",
    "keywords": ["HACCP", "seafood", "contamination"],
    "embedding_index": 0
  },
  {
    "id": "c2_2",
    "norma": "Japón - Food Sanitation Law Art. 11",
    "mercado": "Japón",
    "categoria": "Certificación",
    "año": 2009,
    "descripcion": "...",
    "extracto": "Límites de residuos pesticidas...",
    "keywords": ["pesticidas", "MRL", "alimentos"],
    "embedding_index": 1
  },
  ...
  // Total: 43 normativas
]
```

---

## **ENDPOINT SPECS**

### **POST /search**

**Validaciones:**
- `query`: string no vacío (1-500 chars)
- `top_k`: int 1-43 (default 5)
- `threshold`: float 0-1 (default 0.3)

**Proceso:**
```python
def search(query, top_k, threshold):
    # 1. Validate inputs (10ms)
    # 2. Encode query (50ms)
    # 3. Compute similarities (10ms)
    # 4. Filter & sort (5ms)
    # 5. Format response (5ms)
    # Total: ~80ms
```

**Response:**
- HTTP 200 + JSON
- O HTTP 400 si error validación

---

### **POST /gap-analysis**

**Algoritmo:**
```python
def gap_analysis(query, mercados, top_k):
    gaps = {}
    
    for mercado in mercados:
        # Search en mercado específico
        results = search(
            query=query,
            top_k=top_k,
            filter_by_market=mercado
        )
        gaps[mercado] = results
    
    # Comparar resultados
    return identify_gaps(gaps)
```

---

## **CONSIDERACIONES DE ESCALA**

### **Actualmente**
- 43 normativas
- ~100ms por búsqueda
- Carga en memoria (~15MB)
- 1 usuario sin problemas

### **Para 500 normativas**
- Requerir indexación (FAISS, Pinecone)
- Considerar database (PostgreSQL + pgvector)
- Rate limiting obligatorio
- Caching de queries

### **Para 5000+ normativas**
- Vector database (Weaviate, Milvus)
- Distribuir embeddings
- Implementar batch processing
- API keys + autenticación

---

## **SEGURIDAD (Producción)**

**Actualmente:**
- ❌ CORS abierto (localhost only)
- ❌ Sin autenticación
- ❌ Sin rate limiting
- ❌ Sin logging

**Para Producción:**
```python
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
)

# Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/search")
@limiter.limit("100/minute")
def search(...):
    pass

# Logging
import logging
logger = logging.getLogger(__name__)

# Autenticación
from fastapi.security import HTTPBearer
security = HTTPBearer()
```

---

## **DEPLOYMENT**

### **Local**
```bash
python -m uvicorn main:app --reload --port 8000
```

### **AWS Lambda**
```python
from mangum import Mangum
handler = Mangum(app)
```

### **Docker**
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Kubernetes**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: motor-normativas
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: motor-normativas:2.0
        ports:
        - containerPort: 8000
```

---

## **MONITOREO (Producción)**

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram

search_counter = Counter('searches_total', 'Total searches')
search_latency = Histogram('search_latency_ms', 'Search latency')

@app.post("/search")
def search(...):
    start = time.time()
    search_counter.inc()
    try:
        result = do_search(...)
    finally:
        search_latency.observe((time.time() - start) * 1000)
    return result
```

---

**Última actualización:** 11 Mayo 2026  
**Versión:** 2.0
