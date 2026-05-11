"""
Motor de Evaluación de Impacto Regulatorio Cross-Market
Backend FastAPI con Motor Semántico
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import json

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Motor Evaluación Impacto Regulatorio",
    description="API para análisis semántico de normativas acuícolas",
    version="1.0.0"
)

# CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo semántico (se carga una vez al iniciar)
print("Cargando modelo semántico...")
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
print("✓ Modelo cargado")

# ══════════════════════════════════════════════════════════════════════════════
# CORPUS NORMATIVO
# ══════════════════════════════════════════════════════════════════════════════

CORPUS = [
    # C1 - Acceso y Certificación Sanitaria (8)
    {
        "id": "c1_1",
        "grupo": "C1 - Acceso y Certificación Sanitaria",
        "name": "D.S. 430 - LGPA Exportación",
        "org": "SERNAPESCA",
        "keywords": ["certificado sanitario", "exportacion", "sernapesca", "autorizacion", "habilitacion"],
        "extracto": "Establecimientos exportadores deben contar con certificación sanitaria oficial SERNAPESCA para la exportación de productos pesqueros."
    },
    {
        "id": "c1_2",
        "grupo": "C1 - Acceso y Certificación Sanitaria",
        "name": "Certificado Sanitario MHLW",
        "org": "MHLW Japón",
        "keywords": ["certificado", "mhlw", "japon", "exportacion", "autoridad competente"],
        "extracto": "Japón exige certificado sanitario emitido por SERNAPESCA para cada embarque que valide la aptitud para consumo humano."
    },
    {
        "id": "c1_3",
        "grupo": "C1 - Acceso y Certificación Sanitaria",
        "name": "IN MAPA 1/2017 - Habilitación Planta",
        "org": "MAPA/DIPOA Brasil",
        "keywords": ["habilitacion", "dipoa", "brasil", "mapa", "establecimiento"],
        "extracto": "La habilitación ante DIPOA es un trámite previo único y obligatorio antes de la primera exportación a Brasil."
    },
    {
        "id": "c1_4",
        "grupo": "C1 - Acceso y Certificación Sanitaria",
        "name": "FDA Food Facility Registration",
        "org": "FDA USA",
        "keywords": ["fda", "registro", "facility", "usa", "establecimiento"],
        "extracto": "Todo establecimiento extranjero que exporte alimentos a USA debe estar registrado ante la FDA y renovar cada año par."
    },
    {
        "id": "c1_5",
        "grupo": "C1 - Acceso y Certificación Sanitaria",
        "name": "Autorización de Origen Legal (AOL)",
        "org": "SERNAPESCA",
        "keywords": ["origen legal", "aol", "sernapesca", "acreditacion", "pesca"],
        "extracto": "Documento que acredita que el recurso hidrobiológico ha sido extraído cumpliendo la normativa pesquera y de acuicultura."
    },
    {
        "id": "c1_6",
        "grupo": "C1 - Acceso y Certificación Sanitaria",
        "name": "FSVP - Foreign Supplier Verification",
        "org": "FDA USA",
        "keywords": ["fsvp", "proveedor", "importador", "fda", "verificacion"],
        "extracto": "El importador en USA debe verificar que el proveedor extranjero cumple con los estándares sanitarios aplicables."
    },
    {
        "id": "c1_7",
        "grupo": "C1 - Acceso y Certificación Sanitaria",
        "name": "Licencia Importación LI DIPOA",
        "org": "MAPA/DIPOA Brasil",
        "keywords": ["licencia", "importacion", "brasil", "dipoa", "embarque"],
        "extracto": "Trámite por embarque requerido para ingresar productos pesqueros a Brasil mediante el sistema Siscomex."
    },
    {
        "id": "c1_8",
        "grupo": "C1 - Acceso y Certificación Sanitaria",
        "name": "D.S. 290/1993 - Reglamento Concesiones",
        "org": "SUBPESCA",
        "keywords": ["concesion", "acuicultura", "subpesca", "autorizacion", "centro de cultivo"],
        "extracto": "Regula el otorgamiento de concesiones de acuicultura para operar centros de cultivo en aguas nacionales."
    },

    # C2 - Sanitario e Inocuidad (9)
    {
        "id": "c2_1",
        "grupo": "C2 - Sanitario e Inocuidad",
        "name": "D.S. 977 - Reglamento Sanitario de Alimentos",
        "org": "MINSAL",
        "keywords": ["microorganismos", "patogenos", "salmonella", "listeria", "inocuidad"],
        "extracto": "Control microbiológico de productos pesqueros. Establece límites estrictos para microorganismos patógenos y toxinas."
    },
    {
        "id": "c2_2",
        "grupo": "C2 - Sanitario e Inocuidad",
        "name": "21 CFR Part 123 - HACCP Productos Pesca",
        "org": "FDA USA",
        "keywords": ["haccp", "fda", "pesca", "peligros", "inocuidad"],
        "extracto": "Exige a los procesadores implementar un plan HACCP que controle peligros biológicos, químicos y físicos."
    },
    {
        "id": "c2_3",
        "grupo": "C2 - Sanitario e Inocuidad",
        "name": "Decreto 9.013/2017 RIISPOA",
        "org": "MAPA/DIPOA Brasil",
        "keywords": ["riispoa", "brasil", "parasitos", "microbiologico", "inspeccion"],
        "extracto": "Reglamento de inspección industrial y sanitaria. Exige tolerancia cero para parásitos visibles en pescado."
    },
    {
        "id": "c2_4",
        "grupo": "C2 - Sanitario e Inocuidad",
        "name": "Food Sanitation Act",
        "org": "MHLW Japón",
        "keywords": ["sanitation", "japon", "mhlw", "microorganismos", "parasitos"],
        "extracto": "Establece criterios de inocuidad para alimentos importados en Japón, incluyendo bacterias e inspección de parásitos."
    },
    {
        "id": "c2_5",
        "grupo": "C2 - Sanitario e Inocuidad",
        "name": "D.S. 319/2002 - RESA",
        "org": "SERNAPESCA",
        "keywords": ["resa", "enfermedades", "alto riesgo", "acuicultura", "sanidad"],
        "extracto": "Reglamento de medidas de protección, control y erradicación de enfermedades de alto riesgo en acuicultura."
    },
    {
        "id": "c2_6",
        "grupo": "C2 - Sanitario e Inocuidad",
        "name": "D.S. 345/2005 - REPLA",
        "org": "SERNAPESCA",
        "keywords": ["repla", "plagas", "desinfeccion", "bioseguridad", "mortalidad"],
        "extracto": "Reglamento sobre plagas hidrobiológicas, ensilaje, disposición de mortalidades y bioseguridad en centros."
    },
    {
        "id": "c2_7",
        "grupo": "C2 - Sanitario e Inocuidad",
        "name": "Programa Vigilancia ISA",
        "org": "SERNAPESCA",
        "keywords": ["virus isa", "vigilancia", "salmones", "monitoreo", "epidemiologia"],
        "extracto": "Programa de vigilancia epidemiológica para la detección temprana y control del virus de la Anemia Infecciosa del Salmón."
    },
    {
        "id": "c2_8",
        "grupo": "C2 - Sanitario e Inocuidad",
        "name": "FSMA - Food Safety Modernization Act",
        "org": "FDA USA",
        "keywords": ["fsma", "controles preventivos", "inocuidad", "fda", "peligros"],
        "extracto": "Exige la implementación de controles preventivos basados en riesgo para la inocuidad alimentaria."
    },
    {
        "id": "c2_9",
        "grupo": "C2 - Sanitario e Inocuidad",
        "name": "D.S. 49/2006 - Centros de Acopio",
        "org": "SERNAPESCA",
        "keywords": ["acopio", "faenamiento", "sanidad", "bienestar animal", "desangrado"],
        "extracto": "Establece condiciones sanitarias que deben cumplir los centros de acopio y faenamiento de peces."
    },

    # C3 - Residuos y Medicamentos Veterinarios (8)
    {
        "id": "c3_1",
        "grupo": "C3 - Residuos y Medicamentos Veterinarios",
        "name": "Ley 20.437 - Residuos Antibióticos",
        "org": "SAG / SERNAPESCA",
        "keywords": ["antibioticos", "residuos", "lmr", "medicamentos", "veterinario"],
        "extracto": "Límites Máximos de Residuos para medicamentos veterinarios en productos de acuicultura y fiscalización."
    },
    {
        "id": "c3_2",
        "grupo": "C3 - Residuos y Medicamentos Veterinarios",
        "name": "Antibiotic Residue Tolerance Levels",
        "org": "FDA USA",
        "keywords": ["tolerance", "residue", "fda", "antibioticos", "oxitetraciclina"],
        "extracto": "Niveles de tolerancia de residuos establecidos por FDA para antibióticos en productos pesqueros. Tolerancia cero si no está listado."
    },
    {
        "id": "c3_3",
        "grupo": "C3 - Residuos y Medicamentos Veterinarios",
        "name": "Positive List System (LMR)",
        "org": "MHLW Japón",
        "keywords": ["positive list", "lmr", "japon", "residuos", "mhlw"],
        "extracto": "Sistema de lista positiva japonesa con LMR muy estrictos por especie. Las moléculas no listadas tienen límite automático de 0.01 ppm."
    },
    {
        "id": "c3_4",
        "grupo": "C3 - Residuos y Medicamentos Veterinarios",
        "name": "Programa Residuos PSMB",
        "org": "SERNAPESCA",
        "keywords": ["psmb", "programa sanitario", "residuos", "monitoreo", "moluscos"],
        "extracto": "Programa Sanitario de Moluscos Bivalvos. Monitoreo de biotoxinas marinas, metales pesados y residuos de antibióticos."
    },
    {
        "id": "c3_5",
        "grupo": "C3 - Residuos y Medicamentos Veterinarios",
        "name": "Res. Ex. SAG 3748/2018 - Uso Fármacos",
        "org": "SAG",
        "keywords": ["farmacos", "sag", "prescripcion", "uso responsable", "receta"],
        "extracto": "Regula el uso y prescripción de fármacos en acuicultura. Exige receta y registro de tratamientos."
    },
    {
        "id": "c3_6",
        "grupo": "C3 - Residuos y Medicamentos Veterinarios",
        "name": "Mercosur - LMR Armonizados",
        "org": "Mercosur",
        "keywords": ["mercosur", "armonizacion", "lmr", "acuerdo regional", "brasil"],
        "extracto": "Límites máximos de residuos armonizados entre países del Mercosur para facilitar el comercio regional."
    },
    {
        "id": "c3_7",
        "grupo": "C3 - Residuos y Medicamentos Veterinarios",
        "name": "D.S. 78/2013 - Uso de Antibióticos",
        "org": "SERNAPESCA",
        "keywords": ["antibioticos", "registro", "declaracion", "uso terapeutico", "sernapesca"],
        "extracto": "Exige registro y declaración de uso de antibióticos en centros de cultivo. Control de cantidades utilizadas."
    },
    {
        "id": "c3_8",
        "grupo": "C3 - Residuos y Medicamentos Veterinarios",
        "name": "Codex Stan 193-1995",
        "org": "Codex Alimentarius",
        "keywords": ["codex", "lmr", "internacional", "veterinarios", "armonizacion"],
        "extracto": "Código de prácticas para el pescado y productos pesqueros. Establece LMR internacionales de referencia."
    },

    # C4 - Trazabilidad y Etiquetado (8)
    {
        "id": "c4_1",
        "grupo": "C4 - Trazabilidad y Etiquetado",
        "name": "D.S. 977 Art. 107-120 - Etiquetado",
        "org": "MINSAL",
        "keywords": ["etiquetado", "rotulado", "informacion nutricional", "ingredientes", "alérgenos"],
        "extracto": "Establece requisitos de etiquetado de alimentos: nombre, ingredientes, información nutricional, fecha de vencimiento."
    },
    {
        "id": "c4_2",
        "grupo": "C4 - Trazabilidad y Etiquetado",
        "name": "FDA 21 CFR Part 101 - Food Labeling",
        "org": "FDA USA",
        "keywords": ["food labeling", "fda", "nutrition facts", "allergens", "net quantity"],
        "extracto": "Requisitos de etiquetado USA: Nutrition Facts Panel, declaración de alérgenos, país de origen, net quantity."
    },
    {
        "id": "c4_3",
        "grupo": "C4 - Trazabilidad y Etiquetado",
        "name": "Reg. UE 1169/2011 - Información Alimentaria",
        "org": "Unión Europea",
        "keywords": ["union europea", "etiquetado", "alergenos", "nutricional", "origen"],
        "extracto": "Información obligatoria al consumidor: lista de ingredientes, alérgenos destacados, información nutricional, origen."
    },
    {
        "id": "c4_4",
        "grupo": "C4 - Trazabilidad y Etiquetado",
        "name": "JAS Law - Etiquetado Japón",
        "org": "MAFF Japón",
        "keywords": ["jas", "japon", "etiquetado", "maff", "calidad"],
        "extracto": "Estándares japoneses de calidad y etiquetado. Exige etiqueta en japonés con información detallada de origen y calidad."
    },
    {
        "id": "c4_5",
        "grupo": "C4 - Trazabilidad y Etiquetado",
        "name": "Ley 20.606 - Etiquetado Nutricional (Sellos)",
        "org": "MINSAL",
        "keywords": ["sellos", "alto en", "ley etiquetado", "nutricional", "advertencia"],
        "extracto": "Ley de etiquetado y publicidad de alimentos. Exige sellos de advertencia ALTO EN cuando excede límites de nutrientes críticos."
    },
    {
        "id": "c4_6",
        "grupo": "C4 - Trazabilidad y Etiquetado",
        "name": "FSMA 204 - Food Traceability Rule",
        "org": "FDA USA",
        "keywords": ["traceability", "fsma 204", "fda", "rastreabilidad", "lote"],
        "extracto": "Exige registro digital de datos clave de trazabilidad (KDE) para alimentos de alto riesgo. Vigente desde enero 2026."
    },
    {
        "id": "c4_7",
        "grupo": "C4 - Trazabilidad y Etiquetado",
        "name": "D.S. 977 Art. 121 - Identificación de Lote",
        "org": "MINSAL",
        "keywords": ["lote", "trazabilidad", "identificacion", "fecha elaboracion", "retiro"],
        "extracto": "Todo alimento envasado debe tener identificación de lote que permita rastreo y retiro en caso necesario."
    },
    {
        "id": "c4_8",
        "grupo": "C4 - Trazabilidad y Etiquetado",
        "name": "NCh 2861:2011 - Trazabilidad Productos Pesca",
        "org": "INN Chile",
        "keywords": ["nch 2861", "trazabilidad", "cadena frio", "pesca", "inn"],
        "extracto": "Norma chilena de trazabilidad para productos de la pesca y acuicultura. Establece requisitos de registro en toda la cadena."
    },

    # C5 - Contaminantes y Aditivos (7)
    {
        "id": "c5_1",
        "grupo": "C5 - Contaminantes y Aditivos",
        "name": "D.S. 977 - Límites Metales Pesados",
        "org": "MINSAL",
        "keywords": ["metales pesados", "mercurio", "cadmio", "plomo", "arsenico"],
        "extracto": "Límites máximos para metales pesados en alimentos: mercurio, cadmio, plomo, arsénico."
    },
    {
        "id": "c5_2",
        "grupo": "C5 - Contaminantes y Aditivos",
        "name": "FDA Action Levels - Heavy Metals",
        "org": "FDA USA",
        "keywords": ["action levels", "heavy metals", "mercury", "fda", "fish"],
        "extracto": "Niveles de acción FDA para metales pesados en pescado. Mercurio: 1.0 ppm (mayoría especies), 0.5 ppm (especies menores)."
    },
    {
        "id": "c5_3",
        "grupo": "C5 - Contaminantes y Aditivos",
        "name": "Reg. CE 1881/2006 - Contaminantes",
        "org": "Unión Europea",
        "keywords": ["contaminantes", "union europea", "metales", "dioxinas", "pcb"],
        "extracto": "Contenidos máximos de determinados contaminantes en productos alimenticios: metales pesados, dioxinas, PCB."
    },
    {
        "id": "c5_4",
        "grupo": "C5 - Contaminantes y Aditivos",
        "name": "Codex Stan GSCTFF - Contaminantes",
        "org": "Codex Alimentarius",
        "keywords": ["codex", "contaminantes", "limites", "internacional", "armonizacion"],
        "extracto": "Norma general del Codex para contaminantes y toxinas en alimentos y piensos. Referencia internacional."
    },
    {
        "id": "c5_5",
        "grupo": "C5 - Contaminantes y Aditivos",
        "name": "D.S. 977 - Aditivos Alimentarios",
        "org": "MINSAL",
        "keywords": ["aditivos", "conservantes", "antioxidantes", "autorizados", "dosis maxima"],
        "extracto": "Lista positiva de aditivos alimentarios permitidos y sus dosis máximas en productos pesqueros."
    },
    {
        "id": "c5_6",
        "grupo": "C5 - Contaminantes y Aditivos",
        "name": "FDA 21 CFR Part 172-184 - Food Additives",
        "org": "FDA USA",
        "keywords": ["food additives", "preservatives", "fda", "gras", "permitted"],
        "extracto": "Aditivos alimentarios permitidos por FDA. Incluye lista GRAS (Generally Recognized As Safe) y aditivos directos."
    },
    {
        "id": "c5_7",
        "grupo": "C5 - Contaminantes y Aditivos",
        "name": "Res. Ex. SERNAPESCA 3040/2014 - Histamina",
        "org": "SERNAPESCA",
        "keywords": ["histamina", "intoxicacion", "escombridos", "control", "limites"],
        "extracto": "Control de histamina en especies susceptibles (atún, bonito, jurel). Límite: 50 mg/kg. Plan HACCP obligatorio."
    },

    # ══════════════════════════════════════════════════════════════════════════════
    # C6 - EQUIVALENCIAS REGULATORIAS (DEMO) — 3 NORMAS NUEVAS
    # ══════════════════════════════════════════════════════════════════════════════
    
    {
        "id": "c6_1",
        "grupo": "C6 - Equivalencias Regulatorias",
        "name": "21 CFR Part 123 - Seafood HACCP (USA)",
        "org": "FDA USA",
        "jurisdiccion": "Estados Unidos",
        "producto_aplicable": "Salmón congelado, productos marinos",
        "keywords": [
            "haccp", "seafood", "critical control points", "monitoring", "verification",
            "listeria", "salmonella", "microbiological testing", "sanitation",
            "traceability", "food safety hazards", "quarterly testing", "fda", "guidance"
        ],
        "extracto": """Seafood HACCP and the FDA Food Safety Modernization Act: Guidance for Industry. Regulación que requiere a procesadores implementar planes HACCP escritos. Límites críticos deben controlarse para mitigar peligros de inocuidad alimentaria. Procedimientos de monitoreo en puntos críticos de control incluyen frecuencia de actividades. Verificación mediante revisión de registros cada 7 días. Pruebas microbiológicas para Listeria monocytogenes trimestrales en productos listos para comer. Controles de sanitación documentados. Registro de datos por mínimo 1 año (refrigerados) y 2 años (congelados). Centro para Seguridad de Alimentos y Nutrición Aplicada, FDA, College Park, MD."""
    },
    {
        "id": "c6_2",
        "grupo": "C6 - Equivalencias Regulatorias",
        "name": "Food Sanitation Law Art. 11 - Residuos de Pesticidas (Japón)",
        "org": "MHLW Japón",
        "jurisdiccion": "Japón",
        "producto_aplicable": "Frutas frescas, arándanos, productos agrícolas",
        "keywords": [
            "pesticidas", "residuos", "mrl", "límite máximo residual", "lista positiva",
            "químicos agrícolas", "chlorpyrifos", "certificado fitosanitario",
            "jas", "etiquetado", "pruebas importación", "lotes", "mhlw", "japon", "maff"
        ],
        "extracto": """Pesticide and Food Safety Regulation Update - Japón 2009. Sistema de lista positiva para residuos de químicos agrícolas en alimentos. Límites máximos de residuos (MRLs) establecidos para pesticidas en productos frescos. Límite uniforme de 0.01 ppm para químicos sin estándares específicos. Pruebas requeridas por cada lote importado. Límite Chlorpyrifos para bayas: 0.05 mg/kg. Certificado de análisis acompaña envío. Certificado fitosanitario en formato bilateral. Estándares JAS obligatorios para venta minorista. Trazabilidad a lote de producción. Registro con Ministerio de Agricultura, Silvicultura y Pesca (MAFF) obligatorio."""
    },
    {
        "id": "c6_3",
        "grupo": "C6 - Equivalencias Regulatorias",
        "name": "IN 34/2008 - Certificación Veterinaria Internacional (Brasil)",
        "org": "MAPA/DIPOA Brasil",
        "jurisdiccion": "Brasil",
        "producto_aplicable": "Carnes, productos animales, exportación",
        "keywords": [
            "certificado veterinario", "cvi", "exportacion", "carnes",
            "fiebre aftosa", "peste porcina clásica", "sif", "riispoa",
            "acuerdo bilateral", "inspección federal", "trazabilidad",
            "declaraciones sanitarias", "mapa", "brasil", "dipoa"
        ],
        "extracto": """Estabelece requisitos para certificação veterinária internacional de produtos de origem 
animal destinados à exportação. Certificado Veterinário Internacional (CVI) deve conter 
declarações sanitárias específicas conforme acordo bilateral. Para carne suína: declaração 
de ausência de febre aftosa e peste suína clássica (PPC). Estabelecimento exportador deve 
estar registrado no Serviço de Inspeção Federal (SIF). Auditoria prévia por equipe 
MAPA-país de origem. Rastreabilidade desde origem até destino. Temperatura de transporte 
controlada e documentada. RIISPOA compliance mandatory."""
    }
]

# Pre-computar embeddings del corpus
print("Generando embeddings del corpus...")
corpus_texts = [f"{c['name']} {' '.join(c['keywords'])} {c['extracto']}" for c in CORPUS]
corpus_embeddings = model.encode(
    corpus_texts,
    convert_to_numpy=True,
    normalize_embeddings=True
)
print(f"✓ {len(CORPUS)} normas en memoria")


# ══════════════════════════════════════════════════════════════════════════════
# GRAFO DE EQUIVALENCIAS REGULATORIAS — MOTOR DE GAP ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

EQUIVALENCIAS_REGULATORIAS = {
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHILE → USA (Salmón congelado)
    # ═══════════════════════════════════════════════════════════════════════════
    "CL_USA_SALMON": {
        "norma_origen_id": "c2_1",  # D.S. 977 - Reglamento Sanitario de Alimentos
        "norma_destino_id": "c6_1",  # 21 CFR Part 123
        "producto": "Salmón congelado",
        "cumplimiento_base": 72,  # % que ya cumple Chile
        
        "gaps": [
            {
                "id": "cl_usa_gap_1",
                "categoria": "monitoreo_microbiologico",
                "titulo": "Frecuencia análisis microbiológico",
                "severidad": "alta",
                
                "situacion_actual": {
                    "norma": "DS 977 MINSAL",
                    "descripcion": "Análisis anual de Listeria monocytogenes",
                    "frecuencia": "anual"
                },
                
                "requerido": {
                    "norma": "21 CFR 123.6(c)",
                    "descripcion": "Análisis trimestral + validación de métodos por laboratorio acreditado ISO 17025",
                    "frecuencia": "trimestral"
                },
                
                "accion": {
                    "pasos": [
                        "Contratar laboratorio acreditado ISO 17025",
                        "Implementar calendario de muestreo Q1-Q4",
                        "Documentar métodos de análisis validados",
                        "Mantener registros por 24 meses"
                    ],
                    "responsable": "Jefe de Calidad + Lab externo"
                },
                
                "inversion": {
                    "costo_setup": 0,
                    "costo_anual": 3200,
                    "desglose": "USD 800/análisis × 4 trimestres"
                },
                
                "tiempo": {
                    "implementacion_dias": 5,
                    "descripcion": "Inmediata - solo requiere contratación de servicio"
                },
                
                "impacto_riesgo": "Alto - FDA puede rechazar lote sin este requisito",
                "prioridad": "ALTA"
            },
            
            {
                "id": "cl_usa_gap_2",
                "categoria": "trazabilidad",
                "titulo": "Trazabilidad de cadena de suministro",
                "severidad": "critica",
                
                "situacion_actual": {
                    "norma": "DS 320/2001 SUBPESCA",
                    "descripcion": "Trazabilidad nivel 1: lote de producción en planta",
                    "nivel": "planta"
                },
                
                "requerido": {
                    "norma": "FSMA 204 - Food Traceability Rule",
                    "descripcion": "Traceability lot code hasta proveedor de alimento (feed), smolt, y todos los insumos. Registro digital de cada eslabón accesible en <24 horas",
                    "nivel": "full_supply_chain",
                    "vigencia_obligatoria": "2026-01-20"
                },
                
                "accion": {
                    "pasos": [
                        "Auditar proveedores actuales (feed, smolt, insumos)",
                        "Implementar sistema de trazabilidad backward",
                        "Integrar con ERP existente (módulo supply chain)",
                        "Capacitar equipo en nueva metodología",
                        "Realizar auditoría interna pre-FDA"
                    ],
                    "responsable": "Gerente Operaciones + IT"
                },
                
                "inversion": {
                    "costo_setup": 18000,
                    "costo_anual": 4000,
                    "desglose": "Setup: software USD 12K + consultoría USD 6K | Mantención: USD 4K/año"
                },
                
                "tiempo": {
                    "implementacion_dias": 90,
                    "descripcion": "60 días implementación + 30 días testing + auditoría interna"
                },
                
                "impacto_riesgo": "Crítico - OBLIGATORIO desde enero 2026. Sin esto no se puede exportar a USA",
                "prioridad": "CRÍTICA"
            }
        ],
        
        "roadmap": [
            {"fase": "Semana 1-2", "tarea": "Contratar análisis trimestral Listeria", "responsable": "Calidad"},
            {"fase": "Mes 1", "tarea": "Auditar proveedores actuales", "responsable": "Operaciones"},
            {"fase": "Mes 2", "tarea": "Diseñar sistema trazabilidad backward", "responsable": "IT + Operaciones"},
            {"fase": "Mes 3", "tarea": "Implementar + integrar con ERP", "responsable": "IT"},
            {"fase": "Mes 4", "tarea": "Testing + auditoría interna pre-FDA", "responsable": "Calidad"}
        ],
        
        "resumen_financiero": {
            "inversion_total_ano1": 21200,
            "tiempo_total_dias": 120,
            "cumplimiento_final": 100,
            "revenue_potencial_anual": 2800000,
            "roi": 133
        }
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHILE → JAPÓN (Arándanos frescos)
    # ═══════════════════════════════════════════════════════════════════════════
    "CL_JP_ARANDANOS": {
        "norma_origen_id": "c3_1",  # Ley 20.437 - Residuos Antibióticos (proxy para pesticidas)
        "norma_destino_id": "c6_2",  # Food Sanitation Law Art. 11
        "producto": "Arándanos frescos",
        "cumplimiento_base": 65,
        
        "gaps": [
            {
                "id": "cl_jp_gap_1",
                "categoria": "residuos_pesticidas",
                "titulo": "Límites de residuos de pesticidas",
                "severidad": "critica",
                
                "situacion_actual": {
                    "norma": "SAG - Límites LMR Chile",
                    "descripcion": "Límite Chile para clorpirifós: 0.5 mg/kg",
                    "valor": 0.5,
                    "unidad": "mg/kg"
                },
                
                "requerido": {
                    "norma": "MHLW Positive List System",
                    "descripcion": "Límite Japón para clorpirifós: 0.05 mg/kg (10x más estricto)",
                    "valor": 0.05,
                    "unidad": "mg/kg"
                },
                
                "accion": {
                    "pasos": [
                        "Cambiar a pesticidas en lista positiva MHLW",
                        "Implementar IPM (Integrated Pest Management)",
                        "Realizar análisis de residuos por lote de exportación",
                        "Documentar aplicaciones y tiempos de carencia",
                        "Capacitar equipo técnico en normativa japonesa"
                    ],
                    "responsable": "Agrónomo + Lab"
                },
                
                "inversion": {
                    "costo_setup": 25000,
                    "costo_anual": 12000,
                    "desglose": "Setup: capacitación USD 8K + IPM USD 17K | Análisis: USD 1K/lote × 12 lotes"
                },
                
                "tiempo": {
                    "implementacion_dias": 120,
                    "descripcion": "1 ciclo productivo completo para validar nuevos métodos"
                },
                
                "impacto_riesgo": "Crítico - Japón rechaza 100% de lotes fuera de norma",
                "prioridad": "CRÍTICA"
            },
            
            {
                "id": "cl_jp_gap_2",
                "categoria": "certificacion",
                "titulo": "Certificado fitosanitario formato específico",
                "severidad": "alta",
                
                "situacion_actual": {
                    "descripcion": "Certificado fitosanitario SAG estándar (formato IPPC genérico)"
                },
                
                "requerido": {
                    "norma": "Plant Protection Act + Acuerdo bilateral CL-JP",
                    "descripcion": "Formato bilateral Chile-Japón con declaración adicional de tratamiento cuarentenario específico"
                },
                
                "accion": {
                    "pasos": [
                        "Coordinar con SAG emisión certificado bilateral",
                        "Registrar establecimiento en MAFF (Ministry of Agriculture)",
                        "Implementar protocolo de tratamiento cuarentenario aprobado",
                        "Mantener registros de trazabilidad por 3 años"
                    ]
                },
                
                "inversion": {
                    "costo_setup": 8000,
                    "costo_anual": 2000,
                    "desglose": "Setup: registro MAFF + consultoría | Mantención: USD 2K/año"
                },
                
                "tiempo": {
                    "implementacion_dias": 60,
                    "descripcion": "45 días trámite MAFF + 15 días coordinación SAG"
                },
                
                "prioridad": "ALTA"
            },
            
            {
                "id": "cl_jp_gap_3",
                "categoria": "etiquetado",
                "titulo": "Empaque y etiquetado JAS",
                "severidad": "media",
                
                "situacion_actual": {
                    "descripcion": "Etiqueta en español con información básica"
                },
                
                "requerido": {
                    "norma": "JAS Law (Japan Agricultural Standards)",
                    "descripcion": "Etiqueta en japonés con información nutricional formato JAS, origen, fecha de producción"
                },
                
                "accion": {
                    "pasos": [
                        "Diseñar etiqueta conforme JAS",
                        "Traducción certificada español-japonés",
                        "Aprobación pre-exportación por importador japonés",
                        "Implementar en línea de empaque"
                    ]
                },
                
                "inversion": {
                    "costo_setup": 12000,
                    "costo_anual": 3000,
                    "desglose": "Setup: diseño + traducción + aprobación | Mantención: actualización anual"
                },
                
                "tiempo": {
                    "implementacion_dias": 45,
                    "descripcion": "30 días diseño/traducción + 15 días aprobación"
                },
                
                "prioridad": "MEDIA"
            }
        ],
        
        "roadmap": [
            {"fase": "Mes 1", "tarea": "Cambio a pesticidas lista positiva MHLW", "responsable": "Agrónomo"},
            {"fase": "Mes 2", "tarea": "Registro establecimiento MAFF", "responsable": "Comercio exterior"},
            {"fase": "Mes 2-3", "tarea": "Diseño etiqueta + traducción JAS", "responsable": "Marketing"},
            {"fase": "Mes 3-4", "tarea": "Implementar IPM + protocolo análisis", "responsable": "Agrónomo + Lab"},
            {"fase": "Mes 5", "tarea": "Primer lote piloto exportación", "responsable": "Operaciones"},
            {"fase": "Mes 6", "tarea": "Evaluación resultados + ajustes", "responsable": "Gerencia"}
        ],
        
        "resumen_financiero": {
            "inversion_total_ano1": 45000,
            "tiempo_total_dias": 180,
            "cumplimiento_final": 100,
            "revenue_potencial_anual": 4200000,
            "roi": 93
        }
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHILE → BRASIL (Carne de cerdo)
    # ═══════════════════════════════════════════════════════════════════════════
    "CL_BR_CERDO": {
        "norma_origen_id": "c1_5",  # Autorización de Origen Legal (proxy para sanidad animal)
        "norma_destino_id": "c6_3",  # IN 34/2008
        "producto": "Carne de cerdo",
        "cumplimiento_base": 88,  # Chile ya tiene buen nivel sanitario
        
        "gaps": [
            {
                "id": "cl_br_gap_1",
                "categoria": "certificacion_veterinaria",
                "titulo": "Certificado Veterinario Internacional bilateral",
                "severidad": "alta",
                
                "situacion_actual": {
                    "norma": "SAG - CVI genérico",
                    "descripcion": "Certificado Veterinario Internacional (CVI) genérico emitido por SAG"
                },
                
                "requerido": {
                    "norma": "IN 34/2008 MAPA Art. 7",
                    "descripcion": "CVI formato bilateral Chile-Brasil con declaraciones sanitarias específicas: ausencia de fiebre aftosa en región últimos 12 meses, ausencia de peste porcina clássica (PPC), establecimiento bajo inspección oficial permanente"
                },
                
                "accion": {
                    "pasos": [
                        "Solicitar a SAG emisión de CVI bilateral Chile-Brasil",
                        "Coordinar auditoría conjunta MAPA-SAG de la planta",
                        "Implementar registros de inspección oficial diaria",
                        "Mantener documentación sanitaria por 5 años"
                    ],
                    "responsable": "Médico veterinario oficial + Gerencia"
                },
                
                "inversion": {
                    "costo_setup": 6000,
                    "costo_anual": 2000,
                    "desglose": "Setup: auditoría bilateral USD 5K + trámites USD 1K | Mantención: USD 2K/año"
                },
                
                "tiempo": {
                    "implementacion_dias": 45,
                    "descripcion": "30 días coordinación SAG-MAPA + 15 días auditoría in-situ"
                },
                
                "impacto_riesgo": "Alto - Sin CVI bilateral el lote no ingresa a Brasil",
                "prioridad": "ALTA"
            }
        ],
        
        "roadmap": [
            {"fase": "Semana 1-2", "tarea": "Solicitud formal CVI bilateral a SAG", "responsable": "Comercio exterior"},
            {"fase": "Semana 3-4", "tarea": "Preparación documentación para auditoría", "responsable": "Calidad"},
            {"fase": "Semana 5-6", "tarea": "Auditoría conjunta MAPA-SAG", "responsable": "Gerencia + Vet oficial"},
            {"fase": "Semana 7", "tarea": "Emisión CVI + primer embarque", "responsable": "Logística"}
        ],
        
        "resumen_financiero": {
            "inversion_total_ano1": 8000,
            "tiempo_total_dias": 45,
            "cumplimiento_final": 100,
            "revenue_potencial_anual": 900000,
            "roi": 112
        }
    }
}


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES HELPER: GAP ANALYSIS Y COMPARADOR
# ══════════════════════════════════════════════════════════════════════════════

def obtener_gap_analysis(pais_destino: str, producto: str = None):
    """
    Retorna el análisis de gaps para un país destino específico.
    
    Args:
        pais_destino: 'usa', 'japon', 'brasil'
        producto: opcional, para filtrar por tipo de producto
    
    Returns:
        dict con análisis completo de gaps
    """
    mapping = {
        'usa': 'CL_USA_SALMON',
        'japon': 'CL_JP_ARANDANOS',
        'brasil': 'CL_BR_CERDO'
    }
    
    key = mapping.get(pais_destino.lower())
    if not key:
        return {"error": "País no soportado en demo"}
    
    return EQUIVALENCIAS_REGULATORIAS[key]


def comparar_mercados():
    """
    Retorna comparación de los 3 mercados para decisión estratégica.
    """
    return {
        "usa": {
            "pais": "Estados Unidos",
            "emoji": "🇺🇸",
            "cumplimiento": 72,
            "gaps_criticos": 2,
            "inversion": 21200,
            "tiempo_dias": 120,
            "revenue_potencial": 2800000,
            "roi": 133,
            "recomendacion": 3  # estrellas sobre 4
        },
        "japon": {
            "pais": "Japón",
            "emoji": "🇯🇵",
            "cumplimiento": 65,
            "gaps_criticos": 3,
            "inversion": 45000,
            "tiempo_dias": 180,
            "revenue_potencial": 4200000,
            "roi": 93,
            "recomendacion": 2
        },
        "brasil": {
            "pais": "Brasil",
            "emoji": "🇧🇷",
            "cumplimiento": 88,
            "gaps_criticos": 1,
            "inversion": 8000,
            "tiempo_dias": 45,
            "revenue_potencial": 900000,
            "roi": 112,
            "recomendacion": 4  # quick win
        }
    }


# ══════════════════════════════════════════════════════════════════════════════
# MODELOS PYDANTIC
# ══════════════════════════════════════════════════════════════════════════════

class TextInput(BaseModel):
    texto: str
    
class ClasificacionResponse(BaseModel):
    grupo: str
    confianza: float
    valido: bool
    top_normas: List[Dict]
    
class ImpactoResponse(BaseModel):
    grupo: str
    confianza: float
    valido: bool
    top_normas: List[Dict]
    distribucion: Dict[str, float]
    impacto_usa: Dict
    impacto_japon: Dict
    impacto_brasil: Dict
    conclusion: str

# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES CORE
# ══════════════════════════════════════════════════════════════════════════════

def calcular_similitud(texto: str, corpus_emb: np.ndarray) -> np.ndarray:
    """Calcula similitud coseno entre texto y corpus, normalizada entre -1 y 1"""
    texto_emb = model.encode([texto], convert_to_numpy=True, normalize_embeddings=True)
    corpus_norm = corpus_emb / np.linalg.norm(corpus_emb, axis=1, keepdims=True)
    similitud = np.dot(corpus_norm, texto_emb.T).flatten()
    return similitud

def clasificar_texto(texto: str) -> Dict:
    """Clasifica texto en uno de los 6 grupos normativos (ahora incluye C6)"""
    similitudes = calcular_similitud(texto, corpus_embeddings)
    
    # Agrupar por categoría y promediar
    grupos = {}
    for i, norma in enumerate(CORPUS):
        grupo = norma['grupo']
        if grupo not in grupos:
            grupos[grupo] = []
        grupos[grupo].append(similitudes[i])
    
    # Calcular score por grupo
    grupo_scores = {g: np.mean(scores) for g, scores in grupos.items()}
    
    # Mejor grupo
    mejor_grupo = max(grupo_scores, key=grupo_scores.get)
    confianza = float(grupo_scores[mejor_grupo])
    
    # Validación: confianza mínima 35%
    valido = confianza >= 0.35
    
    # Top 5 normas similares
    indices_top = np.argsort(similitudes)[::-1][:5]
    top_normas = [
        {
            "nombre": CORPUS[i]['name'],
            "org": CORPUS[i]['org'],
            "similitud": float(similitudes[i]),
            "extracto": CORPUS[i]['extracto']
        }
        for i in indices_top
    ]
    
    return {
        "grupo": mejor_grupo if valido else "Sin clasificación",
        "confianza": confianza,
        "valido": valido,
        "top_normas": top_normas,
        "distribucion": {g: float(s) for g, s in grupo_scores.items()}
    }

def evaluar_impacto(clasificacion: Dict) -> Dict:
    """Evalúa impacto regulatorio por mercado usando similitud semántica real del corpus"""
    
    conf = clasificacion['confianza']
    grupo = clasificacion['grupo']
    texto_original = clasificacion.get('texto_original', '')
    
    # Mapeo de organismos por mercado
    MERCADO_ORGS = {
        "USA": ["FDA USA", "FDA", "USDA-AMS USA", "USDA"],
        "Japon": ["MHLW Japón", "MHLW", "CAA/MAFF Japón", "CAA/MAFF"],
        "Brasil": ["MAPA/DIPOA Brasil", "MAPA Brasil", "MAPA/DIPOA", "ANVISA Brasil", "ANVISA"]
    }
    
    # Calcular similitud del texto original contra todo el corpus
    if texto_original:
        similitudes = calcular_similitud(texto_original, corpus_embeddings)
    else:
        similitudes = np.zeros(len(CORPUS))
    
    resultados = {}
    resumen_mercados = []
    
    for mercado, orgs in MERCADO_ORGS.items():
        # Filtrar normas de este mercado
        normas_mercado = []
        for i, norma in enumerate(CORPUS):
            if any(org.lower() in norma['org'].lower() for org in orgs):
                normas_mercado.append((i, norma, float(similitudes[i])))
        
        if normas_mercado:
            # Ordenar por similitud descendente
            normas_mercado.sort(key=lambda x: x[2], reverse=True)
            mejor = normas_mercado[0]
            idx, norma, score = mejor
            
            # Determinar estado según score de similitud
            if score >= 0.65:
                estado = "Cubierto"
                nivel = "Bajo"
                accion = f"Equivalencia alta detectada con {norma['name']}. Verificar vigencia del registro."
            elif score >= 0.45:
                estado = "Parcialmente cubierto"
                nivel = "Medio"
                accion = f"Brecha parcial con {norma['name']}. Revisar requisitos específicos de {mercado} antes del próximo embarque."
            else:
                estado = "No cubierto"
                nivel = "Alto"
                accion = f"Gap regulatorio crítico en {mercado}. No se encontró equivalencia directa con normativa local. Coordinar con Área Legal."
            
            resumen_mercados.append((mercado, nivel, norma['name'], score))
            
            resultados[f"impacto_{mercado.lower()}"] = {
                "estado": estado,
                "riesgo": nivel,
                "impacto": nivel,
                "score": round(score, 4),
                "accion": accion,
                "norma_match": norma['name'],
                "mercado": mercado
            }
        else:
            resumen_mercados.append((mercado, "Alto", "Sin normas en corpus", 0))
            resultados[f"impacto_{mercado.lower()}"] = {
                "estado": "No cubierto",
                "riesgo": "Alto",
                "impacto": "Alto",
                "score": 0,
                "accion": f"No hay normas de {mercado} en el corpus para evaluar equivalencia.",
                "norma_match": "Sin equivalente en corpus",
                "mercado": mercado
            }
    
    # Generar conclusión ejecutiva dinámica
    altos = sum(1 for _, n, _, _ in resumen_mercados if n == "Alto")
    medios = sum(1 for _, n, _, _ in resumen_mercados if n == "Medio")
    
    if altos >= 2:
        conclusion = "Cobertura insuficiente en los tres mercados. Esta normativa presenta brechas regulatorias críticas que requieren acción inmediata del Área Legal antes del próximo embarque."
    elif altos == 1:
        mercado_alto = [m for m, n, _, _ in resumen_mercados if n == "Alto"][0]
        conclusion = f"Brecha regulatoria detectada en {mercado_alto}. Se recomienda validar equivalencia normativa antes de exportar a ese mercado."
    elif medios >= 2:
        conclusion = "Cobertura parcial en múltiples mercados. Revisar requisitos específicos por mercado para asegurar cumplimiento cross-market."
    else:
        conclusion = "Cobertura regulatoria adecuada en los tres mercados principales. Mantener monitoreo de actualizaciones normativas."
    
    resultados["conclusion"] = conclusion
    return resultados

# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/")
def root():
    return {
        "app": "Motor Evaluación Impacto Regulatorio",
        "version": "1.0.0",
        "status": "running",
        "modelo": "paraphrase-multilingual-mpnet-base-v2",
        "corpus_size": len(CORPUS)
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "modelo_cargado": True}

@app.post("/clasificar", response_model=ClasificacionResponse)
def clasificar_normativa(input_data: TextInput):
    """
    Clasifica un texto normativo en uno de los 6 grupos (ahora incluye C6)
    
    Returns:
        - grupo: Grupo normativo detectado
        - confianza: Score de confianza (0-1)
        - valido: Si pasa el umbral mínimo
        - top_normas: 5 normas chilenas más similares
    """
    if not input_data.texto or len(input_data.texto) < 10:
        raise HTTPException(status_code=400, detail="Texto muy corto")
    
    resultado = clasificar_texto(input_data.texto)
    
    return ClasificacionResponse(
        grupo=resultado['grupo'],
        confianza=resultado['confianza'],
        valido=resultado['valido'],
        top_normas=resultado['top_normas']
    )

@app.post("/evaluar_impacto", response_model=ImpactoResponse)
def evaluar_impacto_regulatorio(input_data: TextInput):
    """
    Evalúa el impacto regulatorio cross-market de una normativa
    
    Returns:
        - Clasificación del grupo normativo
        - Impacto por mercado (USA, Japón, Brasil)
        - Conclusión ejecutiva
        - Recomendaciones de acción
    """
    if not input_data.texto or len(input_data.texto) < 10:
        raise HTTPException(status_code=400, detail="Texto muy corto")
    
    # Clasificar
    clasificacion = clasificar_texto(input_data.texto)
    clasificacion['texto_original'] = input_data.texto
    
    # Evaluar impacto
    impacto = evaluar_impacto(clasificacion)
    
    return ImpactoResponse(
        grupo=clasificacion['grupo'],
        confianza=clasificacion['confianza'],
        valido=clasificacion['valido'],
        top_normas=clasificacion['top_normas'],
        distribucion=clasificacion['distribucion'],
        impacto_usa=impacto['impacto_usa'],
        impacto_japon=impacto['impacto_japon'],
        impacto_brasil=impacto['impacto_brasil'],
        conclusion=impacto['conclusion']
    )

@app.get("/corpus")
def obtener_corpus():
    """Retorna el corpus normativo completo"""
    return {"corpus": CORPUS, "total": len(CORPUS)}


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS DEMO — GAP ANALYSIS Y COMPARADOR MULTI-PAÍS
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/api/equivalencias/{pais}")
def get_gap_analysis(pais: str):
    """
    Endpoint para el frontend de la demo.
    GET /api/equivalencias/usa
    GET /api/equivalencias/japon
    GET /api/equivalencias/brasil
    """
    resultado = obtener_gap_analysis(pais)
    
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    
    return resultado


@app.get("/api/comparador")
def get_comparador():
    """
    Endpoint para la vista de comparación multi-país.
    GET /api/comparador
    """
    return comparar_mercados()


# ══════════════════════════════════════════════════════════════════════════════
# EJECUCIÓN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
