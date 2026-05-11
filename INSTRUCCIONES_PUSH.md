# 📤 CÓMO SUBIR LOS CAMBIOS A GITHUB

## Opción 1: Usar GitHub Desktop (Recomendado - Visual)

1. Abre **GitHub Desktop**
2. Selecciona repositorio: `Proyecto-de-normas-acuicola`
3. Deberías ver cambios pendientes:
   ```
   Modified: Proyecto_normas_acuicultura_v2/index.html
   ```

4. En la esquina inferior izquierda, en "Summary (required)" escribe:
   ```
   fix: corregir inconsistencia corpus (43→40 normas)
   ```

5. En "Description" opcionalmente:
   ```
   - Actualizar conteo en UI de 43 a 40 normas reales
   - Agregar archivos del motor v2 (main.py, requirements.txt, README.md)
   ```

6. Presiona **"Commit to main"**

7. En la barra superior, presiona **"Push origin"**

✅ Cambios subidos a GitHub

---

## Opción 2: Usar Terminal

```bash
cd "/Users/felipetirapegui/Desktop/Proyecto de normas acuicola"

# Ver cambios pendientes
git status

# Agregar archivos
git add Proyecto_normas_acuicultura_v2/index.html
git add Proyecto_normas_acuicultura_v2/main.py
git add Proyecto_normas_acuicultura_v2/requirements.txt
git add Proyecto_normas_acuicultura_v2/README.md

# Crear commit
git commit -m "fix: corregir inconsistencia corpus (43→40 normas)"

# Subir a GitHub
git push origin main
```

---

## Opción 3: Script automático

```bash
cd "/Users/felipetirapegui/Desktop/Proyecto de normas acuicola"
bash PUSH_TO_GITHUB.sh
```

---

## Verificar que todo está en GitHub

Después de hacer push:

1. Abre: https://github.com/FelipeTirapegui/Proyecto-de-normas-acuicola
2. En la rama `main`, deberías ver:
   - ✅ `Proyecto_normas_acuicultura_v2/` carpeta
   - ✅ `index.html` con corrección (40 normas)
   - ✅ `main.py` (FastAPI backend)
   - ✅ `requirements.txt`
   - ✅ `README.md`

---

## Troubleshooting

### "fatal: Unable to create '.git/index.lock'"
Solución:
```bash
rm -f .git/index.lock
git status
```

### "Permission denied"
Solución: Usar GitHub Desktop en lugar de Terminal

### "Nothing to commit"
Significa que no hay cambios nuevos. Verifica que editaste los archivos correctamente.

---

## Confirmación final

Una vez hecho push, comparte la URL:
```
https://github.com/FelipeTirapegui/Proyecto-de-normas-acuicola
```

Y verifica que:
- [x] Código del motor v2 está visible
- [x] `index.html` muestra "40 normas" (no 43)
- [x] Commit message es claro

¡Listo! 🚀
