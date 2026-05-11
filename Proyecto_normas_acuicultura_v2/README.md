# 🌍 Motor de Búsqueda Semántica de Normativas

**Clasificador inteligente de regulaciones HSEC para industrias reguladas en LATAM**

---

## ¿Qué es?

Motor de búsqueda semántica que permite:
- 🔍 **Buscar normativas por similitud** (no solo palabras clave)
- 📊 **Gap analysis automático** entre regulaciones de 4 mercados
- 🎯 **Identificar requisitos regulatorios cruzados**
- 📈 **Analizar impacto de compliance en operaciones**

Cubre **43 normativas** de USA, Japón, Brasil y mercados LATAM en SST, ambiental, permisología y certificación.

---

## Stack Técnico

| Componente | Tecnología |
|-----------|-----------|
| **Backend** | FastAPI + Python |
| **Embeddings** | sentence-transformers (paraphrase-multilingual-mpnet-base-v2) |
| **Búsqueda** | Similitud de coseno |
| **Frontend** | HTML5 + Vanilla JavaScript |
| **Vectores** | Embeddings pre-computados en .npy |

---

## Instalación Rápida

### **Requisitos**
- Python 3.8+
- pip

### **1. Clonar el repo**
```bash
git clone https://github.com/FelipeTirapegui/Proyecto-de-normas-acuicola.git
cd Proyecto-de-normas-acuicola/Proyecto_normas_acuicultura_v2
```

### **2. Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **3. Correr el backend**
```bash
python -m uvicorn main:app --reload --port 8000
```

Deberías ver:
```
✓ Uvicorn running on http://127.0.0.1:8000
✓ Modelo cargado
✓ 43 normas en memoria
```

### **4. Abrir el frontend**
```bash
# En otro terminal, abre el archivo HTML:
open index.html
```

O navega a:
```
file:///[TU_RUTA]/Proyecto_normas_acuicultura_v2/index.html
```

---

## Uso

### **Búsqueda Semántica**
1. Escribe un requisito regulatorio (ej: "residuos pesticidas en alimentos")
2. El motor busca normativas similares en los 43 documentos
3. Retorna coincidencias con score de similitud (0-100)

### **Gap Analysis**
1. Selecciona 2+ mercados
2. El motor compara regulaciones
3. Identifica brechas y requisitos únicos

### **Corpus**
- **40 normativas base** + **3 PDFs integrados**
- Incluye: 21 CFR (USA), Food Sanitation Law (Japón), IN 34/2008 (Brasil)
- Cubiertos: SST, Ambiental, Permisología, Certificación

---

## Estructura de Carpetas

```
Proyecto_normas_acuicultura_v2/
├── main.py                 # Backend FastAPI
├── index.html              # Frontend
├── requirements.txt        # Dependencias
├── README.md               # Esta documentación
├── embeddings.npy          # Vectores pre-computados
├── embeddings_indice.json  # Mapeo de índices
└── corpus_stats.json       # Metadata del corpus
```

---

## API Endpoints

### **POST /search**
Busca normativas similares a un query.

**Request:**
```json
{
  "query": "requisitos de etiquetado de productos acuícolas",
  "top_k": 5,
  "threshold": 0.3
}
```

**Response:**
```json
{
  "resultados": [
    {
      "norma": "Japón - Food Sanitation Law Art. 11",
      "similitud": 0.87,
      "mercado": "Japón",
      "extracto": "..."
    }
  ],
  "tiempo_ms": 145
}
```

### **GET /corpus**
Obtiene metadata del corpus.

**Response:**
```json
{
  "total_normas": 43,
  "mercados": ["USA", "Japón", "Brasil", "LATAM"],
  "categorias": ["SST", "Ambiental", "Permisología", "Certificación"]
}
```

### **POST /gap-analysis**
Compara regulaciones entre mercados.

**Request:**
```json
{
  "query": "límites de emisión de CO2",
  "mercados": ["USA", "Brasil"],
  "top_k": 3
}
```

---

## Próximos Pasos

### **Testing**
- [ ] Validar búsquedas semánticas con casos reales
- [ ] Verificar gap analysis con equipo legal/ambiental
- [ ] Probar con datos de clientes piloto

### **Mejoras**
- [ ] Agregar más normativas (EU, Canadá, etc.)
- [ ] Integrar base de datos para persistencia
- [ ] Dashboard de KPIs (adopción, queries, tiempo respuesta)
- [ ] API de webhooks para alertas regulatorias

### **Productivización**
- [ ] Deploy a servidor (AWS/GCP/Azure)
- [ ] Autenticación y control de acceso
- [ ] Logging y monitoreo
- [ ] Documentación de SLA

---

## Support

Preguntas frecuentes en `FAQ.md` (próximamente)

Para reportar bugs o sugerencias, abre un issue en GitHub.

---

**Versión**: 2.0  
**Última actualización**: 11 Mayo 2026  
**Estado**: Operativo
