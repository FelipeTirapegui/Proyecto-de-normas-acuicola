# ⚡ Quick Start - 5 Minutos

Levanta el motor de normativas en menos de 5 minutos.

---

## **Paso 1: Descargar (30 segundos)**

```bash
git clone https://github.com/FelipeTirapegui/Proyecto-de-normas-acuicola.git
cd Proyecto-de-normas-acuicola/Proyecto_normas_acuicultura_v2
```

---

## **Paso 2: Instalar dependencias (2 minutos)**

```bash
pip install -r requirements.txt
```

**Qué se instala:**
- fastapi
- uvicorn
- sentence-transformers
- torch
- numpy

---

## **Paso 3: Correr el backend (30 segundos)**

Abre una terminal Y escribe:

```bash
python -m uvicorn main:app --reload --port 8000
```

**Espera a ver esto:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✓ Modelo cargado
✓ 43 normas en memoria
```

✅ **Backend está listo**

---

## **Paso 4: Abrir el frontend (30 segundos)**

**Opción A - Desde terminal (recomendado):**
```bash
open index.html
```

**Opción B - Manual:**
- Abre el Finder/Explorador
- Busca `index.html` en la carpeta
- Doble clic para abrir en navegador

✅ **Deberías ver la interfaz con "43 normas"**

---

## **Paso 5: Prueba una búsqueda (1 minuto)**

En el campo de búsqueda, escribe:
```
residuos pesticidas en alimentos
```

Presiona Enter. Deberías ver:
- 5 normativas similares
- Scores de similitud (0-100)
- País de origen

---

## **¡Listo! 🎉**

Tu motor está operativo. Ahora:

1. **Prueba gap analysis** → Selecciona 2 países
2. **Explora el corpus** → Haz clic en "CORPUS NORMATIVO"
3. **Lee la documentación completa** → Ver `README.md`

---

## **Troubleshooting**

### ❌ "No se pudo conectar con el backend"
**Solución:** Verifica que ejecutaste el paso 3. FastAPI debe estar corriendo en `http://127.0.0.1:8000`

### ❌ "ModuleNotFoundError: No module named 'fastapi'"
**Solución:** Ejecuta `pip install -r requirements.txt` nuevamente

### ❌ "Port 8000 already in use"
**Solución:** Cambia el puerto:
```bash
python -m uvicorn main:app --reload --port 8001
```

Luego abre el navegador en `http://127.0.0.1:8001`

---

**¿Necesitas ayuda?** Ver `README.md` para documentación completa.
