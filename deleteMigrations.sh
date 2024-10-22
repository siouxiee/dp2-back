#!/bin/bash

# Ruta al directorio raíz de tu proyecto Django
PROJECT_DIR="./"

# Obtener la lista de carpetas "__pycache__" en el proyecto
PYCACHE_DIRS=$(find "$PROJECT_DIR" -type d -name "__pycache__")

# Eliminar las carpetas "__pycache__"
for DIR in $PYCACHE_DIRS; do
  rm -rf "$DIR"
done

# Obtener la lista de aplicaciones en el proyecto
APP_DIRS=$(find "$PROJECT_DIR" -type d -name "migrations")

# Recorrer cada directorio de migraciones de las aplicaciones
for APP_DIR in $APP_DIRS; do
  # Excluir el archivo __init__.py y las carpetas env, venv
  FILES_TO_DELETE=$(find "$APP_DIR" -type f ! -name "__init__.py" ! -path "*/env/*" ! -path "*/venv/*" ! -path "*/.venv/*")

  # Eliminar los archivos
  if [ -n "$FILES_TO_DELETE" ]; then
    rm -f $FILES_TO_DELETE
  fi

  # Eliminar las carpetas de migraciones vacías
  #find "$APP_DIR" -type d -empty -delete
done

echo "Contenido de las carpetas migrations eliminado exitosamente en todas las aplicaciones del proyecto."
