# 📡 API Documentation

Referencia completa de endpoints disponibles.

---

## **Base URL**

```
http://127.0.0.1:8000
```

Todos los ejemplos usan esta URL base.

---

## **1. Search - Búsqueda Semántica**

### **Endpoint**
```
POST /search
```

### **Descripción**
Busca normativas similares a un query usando similitud semántica.

### **Request**

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "query": "límites máximos de residuos pesticidas",
  "top_k": 5,
  "threshold": 0.3
}
```

**Parámetros:**
| Param | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| query | string | Sí | Requisito regulatorio o pregunta |
| top_k | int | No | Top K resultados (default: 5) |
| threshold | float | No | Score mínimo (0-1, default: 0.3) |

### **Response**

**Status:** `200 OK`

```json
{
  "resultados": [
    {
      "id": "c2_2",
      "norma": "Japón - Food Sanitation Law Art. 11 (Residuos de Pesticidas)",
      "mercado": "Japón",
      "categoria": "Certificación",
      "similitud": 0.87,
      "extracto": "Establece límites máximos de residuos (MRL) para pesticidas en alimentos. Aplica lista positiva de pesticidas autorizados...",
      "keywords": ["pesticidas", "residuos", "MRL", "límites", "alimentos"]
    },
    {
      "id": "c1_3",
      "norma": "USA - 21 CFR Part 123 (Seafood HACCP)",
      "mercado": "USA",
      "categoria": "SST",
      "similitud": 0.64,
      "extracto": "Establece sistema HACCP obligatorio para productos del mar...",
      "keywords": ["HACCP", "seafood", "contaminación", "seguridad"]
    }
  ],
  "tiempo_ms": 145,
  "total_resultados": 2
}
```

### **Ejemplo cURL**

```bash
curl -X POST "http://127.0.0.1:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "residuos pesticidas",
    "top_k": 5,
    "threshold": 0.3
  }'
```

### **Casos de Uso**

```
❶ "requisitos de etiquetado de productos acuícolas"
❷ "límites de descarga de efluentes"
❸ "certificación de sostenibilidad ambiental"
❹ "protocolo de inspección de calidad"
❺ "documento de trazabilidad obligatorio"
```

---

## **2. Corpus - Metadata del Motor**

### **Endpoint**
```
GET /corpus
```

### **Descripción**
Retorna información sobre el corpus de normativas disponibles.

### **Request**

Sin body.

### **Response**

**Status:** `200 OK`

```json
{
  "total_normas": 43,
  "mercados": [
    {
      "nombre": "USA",
      "total": 12,
      "categorias": ["SST", "Ambiental", "Permisología"]
    },
    {
      "nombre": "Japón",
      "total": 8,
      "categorias": ["Certificación", "Ambiental"]
    },
    {
      "nombre": "Brasil",
      "total": 10,
      "categorias": ["Permisología", "SST"]
    },
    {
      "nombre": "LATAM",
      "total": 13,
      "categorias": ["Ambiental", "SST", "Certificación"]
    }
  ],
  "categorias": [
    {
      "nombre": "SST",
      "total": 15,
      "descripcion": "Seguridad y Salud en el Trabajo"
    },
    {
      "nombre": "Ambiental",
      "total": 12,
      "descripcion": "Regulaciones ambientales y emisiones"
    },
    {
      "nombre": "Permisología",
      "total": 8,
      "descripcion": "Permisos, licencias y RCA"
    },
    {
      "nombre": "Certificación",
      "total": 8,
      "descripcion": "Certificaciones obligatorias"
    }
  ],
  "version": "2.0",
  "fecha_actualizacion": "2026-05-11"
}
```

### **Ejemplo cURL**

```bash
curl -X GET "http://127.0.0.1:8000/corpus"
```

---

## **3. Gap Analysis - Comparación Entre Mercados**

### **Endpoint**
```
POST /gap-analysis
```

### **Descripción**
Compara regulaciones de un tema específico entre 2+ mercados.

### **Request**

**Body:**
```json
{
  "query": "límites de emisión de CO2",
  "mercados": ["USA", "Brasil"],
  "top_k": 3
}
```

**Parámetros:**
| Param | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| query | string | Sí | Tema a comparar |
| mercados | array | Sí | Lista de mercados (min: 2) |
| top_k | int | No | Top K resultados por mercado (default: 3) |

### **Response**

**Status:** `200 OK`

```json
{
  "query": "límites de emisión de CO2",
  "gap_analysis": [
    {
      "mercado": "USA",
      "normativas": [
        {
          "norma": "Clean Air Act",
          "similitud": 0.92,
          "requisito": "Límites de 500 ppm CO2..."
        }
      ]
    },
    {
      "mercado": "Brasil",
      "normativas": [
        {
          "norma": "CONAMA Resolução 420/2009",
          "similitud": 0.78,
          "requisito": "Valores máximos de 1500 ppm..."
        }
      ]
    }
  ],
  "brechas": [
    {
      "tipo": "Diferencia en límites",
      "descripcion": "USA es 3x más restrictivo que Brasil"
    }
  ]
}
```

---

## **4. Health Check - Estado del Motor**

### **Endpoint**
```
GET /health
```

### **Descripción**
Verifica que el motor esté operativo.

### **Response**

**Status:** `200 OK`

```json
{
  "status": "ok",
  "modelo": "paraphrase-multilingual-mpnet-base-v2",
  "normas_en_memoria": 43,
  "version": "2.0"
}
```

---

## **Error Handling**

### **Errores Comunes**

**400 Bad Request**
```json
{
  "detail": "Query requerido"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Error al procesar embeddings"
}
```

---

## **Rate Limiting**

- **Sin límite** para desarrollo local
- En producción: Implementar rate limiting (recomendado: 100 req/min)

---

## **Ejemplos en Python**

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Search
response = requests.post(
    f"{BASE_URL}/search",
    json={
        "query": "residuos pesticidas",
        "top_k": 5,
        "threshold": 0.3
    }
)
print(response.json())

# Corpus info
response = requests.get(f"{BASE_URL}/corpus")
print(response.json())
```

---

## **Ejemplos en JavaScript**

```javascript
const BASE_URL = "http://127.0.0.1:8000";

// Search
fetch(`${BASE_URL}/search`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "residuos pesticidas",
    top_k: 5,
    threshold: 0.3
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

**Última actualización:** 11 Mayo 2026
