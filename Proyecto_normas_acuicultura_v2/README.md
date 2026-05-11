# Motor de Evaluación de Impacto Regulatorio Cross-Market

Sistema de análisis semántico de normativas acuícolas para evaluación de riesgo regulatorio en mercados de exportación (USA, Japón, Brasil).

## 🎯 Objetivo

Permitir a empresas acuícolas chilenas evaluar el impacto regulatorio de nuevas normativas antes de iniciar exportaciones, identificando brechas normativas y riesgos de cumplimiento.

## 📁 Estructura del Proyecto

```
Proyecto_normas_acuicultura_v2/
├── backend/           # API FastAPI + Motor Semántico Python
├── frontend/          # Interface HTML/JS
├── notebooks/         # Jupyter notebooks para desarrollo
├── data/             # Corpus normativo y datos
└── docs/             # Documentación
```

## 🚀 Stack Técnico

- **Backend**: Python 3.10+ | FastAPI | sentence-transformers
- **Frontend**: HTML5 | Vanilla JS | CSS3
- **ML Model**: paraphrase-multilingual-mpnet-base-v2 (768 dim)
- **Deployment**: Railway / Render / Fly.io

## 📊 Características

- ✅ Clasificación semántica de normativas en 5 grupos
- ✅ Análisis de similitud con corpus de 40 normas chilenas
- ✅ Evaluación de impacto cross-market (USA, Japón, Brasil)
- ✅ Detección de brechas regulatorias por mercado
- ✅ Recomendaciones de acción para área legal

## 🔧 Setup Rápido

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Frontend
cd frontend
# Abrir index.html en browser
```

## 📝 Autores

**m-risk** - Beyond Sustainability
