#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Copy committed media files to Persistent Disk (if configured)
SCRIPT_DIR="$(dirname "$0")"
if [ -n "$MEDIA_ROOT" ] && [ "$MEDIA_ROOT" != "$SCRIPT_DIR/media" ]; then
    echo "Copying repository media files to $MEDIA_ROOT..."
    mkdir -p "$MEDIA_ROOT/productos" "$MEDIA_ROOT/categorias"
    cp -rn "$SCRIPT_DIR/media/productos/"* "$MEDIA_ROOT/productos/" 2>/dev/null || true
    cp -rn "$SCRIPT_DIR/media/categorias/"* "$MEDIA_ROOT/categorias/" 2>/dev/null || true
fi

# Asignar imágenes a productos (FileSystemStorage local / Cloudinary en producción)
python manage.py arreglar_imagenes
