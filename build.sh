#!/usr/bin/env bash
# build.sh — script de build para Render

set -o errexit  # hace que falle si algún comando falla

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate --noinput

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
