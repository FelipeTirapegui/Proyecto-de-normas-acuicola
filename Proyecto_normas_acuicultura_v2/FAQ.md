# ❓ FAQ - Preguntas Frecuentes

Respuestas a las preguntas más comunes sobre el motor.

---

## **INSTALACIÓN & SETUP**

### **P: ¿Puedo usar Windows?**
**R:** Sí, los pasos son idénticos. Solo asegúrate de tener Python 3.8+ instalado.

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### **P: ¿Necesito GPU?**
**R:** No. El motor es CPU-only. Funciona perfecto en cualquier laptop con Python.

- CPU: 10-100ms por búsqueda
- GPU (opcional): <5ms por búsqueda

### **P: ¿Cuánto espacio en disco?**
**R:** ~50MB total (incluye embeddings pre-computados)

- `embeddings.npy`: ~13MB
- `main.py`: ~50KB
- Resto: ~36MB

### **P: ¿Cómo cambio el puerto 8000?**
**R:**
```bash
python -m uvicorn main:app --reload --port 8001
```

Luego en `index.html`, busca `http://127.0.0.1:8000` y cámbialo a `8001`.

---

## **BÚSQUEDA & RESULTADOS**

### **P: ¿Por qué no me retorna resultados para mi query?**
**R:** Posibles razones:

1. **Threshold muy alto** → Baja el threshold (default 0.3)
   ```json
   {"query": "test", "threshold": 0.1}
   ```

2. **Query muy específico** → Intenta palabras clave generales
   - ❌ "Artículo 7 párrafo 3 inciso a" 
   - ✅ "límites de emisión"

3. **Idioma incorrecto** → El modelo es multilingüe, pero funciona mejor con español puro
   - ❌ "compliance requirements seafood HACCP"
   - ✅ "requisitos HACCP para productos del mar"

### **P: ¿Cómo interpreto el score de similitud?**
**R:**

| Score | Interpretación |
|-------|-----------------|
| 0.9-1.0 | Altamente relevante |
| 0.7-0.9 | Muy relevante |
| 0.5-0.7 | Medianamente relevante |
| 0.3-0.5 | Moderadamente relevante |
| <0.3 | Débilmente relevante |

### **P: ¿Puedo hacer búsquedas muy largas?**
**R:** Sí, hasta 500 caracteres. Pero las búsquedas cortas (5-20 palabras) funcionan mejor.

- ❌ "Dame todas las normativas sobre residuos que aplican a la acuicultura en Japón, Brasil y USA considerando..."
- ✅ "Normativas residuos acuicultura Japón"

### **P: ¿Los resultados son exactos?**
**R:** No. Son **semánticamente relevantes**, no exactos.

- El motor busca **significado**, no palabras clave
- Ejemplo: "residuos pesticidas" también retorna "limitaciones químicas"
- Esto es una **ventaja** para descubrir regulaciones relacionadas

### **P: ¿Cómo hago gap analysis?**
**R:** 

1. Selecciona 2+ países en el modal
2. Escribe tu query
3. Presiona "Gap Analysis"
4. El motor compara normativas de cada país

---

## **DATOS & CORPUS**

### **P: ¿Cuántas normativas hay?**
**R:** 43 actualmente

Desglose:
- USA: 12
- Japón: 8
- Brasil: 10
- LATAM: 13

### **P: ¿Qué significa cada categoría?**

| Categoría | Descripción |
|-----------|------------|
| **SST** | Seguridad y Salud en el Trabajo |
| **Ambiental** | Regulaciones ambientales, emisiones, agua |
| **Permisología** | Permisos, licencias, RCA, EIA |
| **Certificación** | Certificaciones obligatorias, trazabilidad |

### **P: ¿Puedo agregar mis propias normativas?**
**R:** Sí, pero requiere cambios en código:

1. Edita `main.py`
2. Agrega entrada a `CORPUS`
3. Calcula embedding con `SentenceTransformer`
4. Actualiza `embeddings.npy`

(Documentación de esto próximamente)

### **P: ¿Dónde obtienen las normativas del motor?**
**R:** Son extractos de:
- Sitios de gobiernos (EPA, MAPA, etc.)
- Bases de datos regulatorias
- PDFs de reguladores oficiales
- Consultoría legal

**Nota:** Revisar siempre con legal/ambiental antes de actuar.

### **P: ¿Las normativas se actualizan?**
**R:** Actualmente NO son automáticas. Se actualizan manually:

1. Detectar cambio regulatorio
2. Extraer nuevo contenido
3. Actualizar `CORPUS` en `main.py`
4. Recomputar embeddings
5. Comitear a GitHub

---

## **API & INTEGRACIÓN**

### **P: ¿Puedo usar la API desde mi app?**
**R:** Sí. Cualquier lenguaje que hable HTTP puede usarla.

**Python:**
```python
import requests
response = requests.post(
    "http://127.0.0.1:8000/search",
    json={"query": "residuos pesticidas", "top_k": 5}
)
print(response.json())
```

**JavaScript:**
```javascript
fetch("http://127.0.0.1:8000/search", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({query: "residuos pesticidas", top_k: 5})
})
.then(r => r.json())
.then(data => console.log(data));
```

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"residuos pesticidas","top_k":5}'
```

### **P: ¿Qué límite de rate limiting hay?**
**R:** Actualmente **NINGUNO** (desarrollo local).

En producción se recomienda:
- 100 requests/minuto por usuario
- 10,000 requests/día por plan

### **P: ¿Los datos viajan cifrados?**
**R:** No en desarrollo (localhost).

En producción, implementar:
```python
# SSL/TLS
# HTTPS obligatorio
# Encriptación de datos sensibles
```

---

## **PERFORMANCE**

### **P: ¿Por qué tarda 500ms en responder?**
**R:** Desglose típico:

| Operación | Tiempo |
|-----------|--------|
| Validación | 5ms |
| Encoding query | 50ms |
| Similitud coseno (43x) | 10ms |
| Filtrado + sorting | 5ms |
| Serialización JSON | 10ms |
| **Total** | **~80ms** |

Si ves >500ms:
1. Verifica tu conexión
2. Comprueba CPU disponible
3. Revisa si hay otros procesos

### **P: ¿Cómo optimizo la velocidad?**
**R:**

**Opción 1: Indexación** (para 500+ normas)
```python
from faiss import IndexFlatL2
index = IndexFlatL2(384)
index.add(embeddings)
```

**Opción 2: Caché** (para queries repetidas)
```python
@cache
def search(query, top_k, threshold):
    # ...
```

**Opción 3: Vector DB** (para escala)
```python
# Usar Pinecone, Weaviate, Milvus
```

---

## **ERRORS & TROUBLESHOOTING**

### **P: "No se pudo conectar con el backend"**
**R:** El navegador no puede alcanzar `http://127.0.0.1:8000`

**Soluciones:**
1. ¿Ejecutaste `python -m uvicorn main:app --reload --port 8000`?
2. ¿El puerto 8000 está libre? (`lsof -i :8000`)
3. ¿Esperas a ver "Uvicorn running"?

### **P: "ModuleNotFoundError: No module named 'sentence_transformers'"**
**R:** Las dependencias no están instaladas.

```bash
pip install -r requirements.txt
```

### **P: "Port 8000 already in use"**
**R:** Algo más está usando ese puerto.

```bash
# Matar proceso en puerto 8000
lsof -ti :8000 | xargs kill -9

# O usar otro puerto
python -m uvicorn main:app --reload --port 8001
```

### **P: Frontend carga pero búsqueda no funciona**
**R:** Probablemente error de CORS.

**Solución:**
1. Abre DevTools (F12)
2. Ve a Console
3. Busca "CORS" en los errores
4. Verifica que FastAPI esté corriendo

### **P: ¿Cómo veo los logs de FastAPI?**
**R:** Aparecen en la terminal donde ejecutas:

```bash
python -m uvicorn main:app --reload --port 8000
```

Deberías ver:
```
INFO:     127.0.0.1:54321 - "POST /search HTTP/1.1" 200 OK
```

---

## **DATOS & PRIVACIDAD**

### **P: ¿Dónde se guardan los datos que busco?**
**R:** En desarrollo = solo memoria (no persiste).

En producción, implementar:
```python
# Logging de queries
# Auditoría
# Cumplimiento GDPR
```

### **P: ¿Puedo usar datos de clientes reales?**
**R:** Sí, pero considera:

1. ✅ Normativas públicas = usar directamente
2. ⚠️ Datos de cliente = cifrar, auditar acceso
3. 🔒 Información sensible = no almacenar localmente

---

## **SOPORTE & CONTACTO**

### **P: ¿Dónde reporte bugs?**
**R:** GitHub Issues

https://github.com/FelipeTirapegui/Proyecto-de-normas-acuicola/issues

**Formato:**
```
Título: [BUG] Búsqueda retorna 0 resultados
Descripción: 
- Query: "residuos pesticidas"
- Esperado: 3+ resultados
- Obtenido: 0 resultados
- Entorno: Mac, Python 3.9, FastAPI 0.95
```

### **P: ¿Hay documentación adicional?**
**R:** Sí:
- `README.md` - General
- `QUICKSTART.md` - Setup rápido
- `API_DOCS.md` - Endpoints
- `ARCHITECTURE.md` - Técnico
- `TESTING_CHECKLIST.md` - Testing
- `HANDOFF.md` - Para clientes

### **P: ¿Puedo contribuir al proyecto?**
**R:** Sí, fork del repo y haz pull requests.

Áreas de contribución:
- Agregar normativas
- Mejorar UI
- Optimizar búsqueda
- Documentación

---

## **PRÓXIMOS PASOS**

### **P: ¿Qué viene después?**
**R:** Roadmap provisional:

**Q3 2026:**
- Database persistente
- Autenticación de usuarios
- Dashboard de uso

**Q4 2026:**
- Alertas regulatorias automáticas
- Integración con Slack/Teams
- Analytics avanzado

**2027:**
- Predicciones de cambios normativos
- AI-powered gap analysis
- Benchmarking inter-industria

---

**Última actualización:** 11 Mayo 2026  
**Mantenido por:** Technical Team
