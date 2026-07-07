# E-Commerce M7

Plataforma de comercio electrónico profesional construida con Django 6 y Bootstrap 5. Catálogo de productos con imágenes, carrito de compras híbrido (sesión/usuarios), checkout con descuento de stock, historial de pedidos, autenticación de usuarios y panel de administración completo.

---

## 1. Descripción del proyecto

**E-Commerce M7** es una aplicación web full-stack desarrollada como proyecto de portafolio. Implementa las funcionalidades esenciales de una tienda online real.

### Funcionalidades principales

- Catálogo de productos con buscador, filtros (categoría, precio, disponibilidad) y ordenamiento
- Carrito de compras híbrido: asociado a sesión para visitantes anónimos y a usuario para clientes registrados
- Checkout transaccional con validación de stock, descuento automático y confirmación de pedido
- Historial de pedidos con seguimiento de estados (pendiente → preparación → enviado → entregado)
- Autenticación completa: registro, inicio/cierre de sesión, perfil de usuario
- Panel de administración para staff con CRUD completo de productos
- Panel Django Admin personalizado con inlines, filtros y edición en línea
- Diseño responsive con Bootstrap 5, animaciones y breadcrumbs

### Tecnologías utilizadas

| Categoría | Tecnología | Versión |
|-----------|-----------|---------|
| Backend | Django | 6.0.6 |
| Lenguaje | Python | 3.12.1 |
| Base de datos (dev) | SQLite | — |
| Base de datos (prod) | PostgreSQL | 15+ |
| Frontend | Bootstrap | 5.3.3 |
| Iconos | Bootstrap Icons | 1.11.3 |
| Imágenes | Pillow | 12.3.0 |
| Servidor (prod) | Gunicorn | 23.0.0 |
| Estáticos (prod) | WhiteNoise | 6.12.0 |
| Imágenes (opt.) | Cloudinary | — |

---

## 2. Repositorio público

```
https://github.com/tu-usuario/ecommerce-m7
```

> Si el repositorio aún no existe, créalo en [GitHub](https://github.com/new) con el nombre `ecommerce-m7` y sigue las instrucciones de la sección **Instalación**.

---

## 3. Requisitos

### Sistema operativo

- Linux (Recomendado para producción)
- macOS
- Windows (WSL recomendado)

### Software requerido

| Componente | Versión mínima |
|-----------|----------------|
| Python | 3.12.1 |
| pip | 24+ (incluido con Python) |
| PostgreSQL | 15+ (opcional, solo para producción) |

### Dependencias Python

Todas las dependencias están listadas en `requirements.txt`:

| Paquete | Versión | Requerido |
|---------|---------|-----------|
| Django | 6.0.6 | Sí |
| pillow | 12.3.0 | Sí |
| whitenoise | 6.12.0 | Sí |
| gunicorn | 23.0.0 | Sí (producción) |
| psycopg2-binary | 2.9.12 | Sí (PostgreSQL) |
| dj-database-url | 3.1.2 | Sí (PostgreSQL) |
| django-cloudinary-storage | 0.3.0 | Opcional |
| sqlparse | 0.5.5 | Dependencia interna |

> `django-cloudinary-storage` y `cloudinary` son **opcionales**. Solo se necesitan si se configura almacenamiento de imágenes en Cloudinary. Sin ellas, las imágenes se sirven desde el sistema de archivos local.

---

## 4. Instalación

### 4.1 Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/ecommerce-m7.git
cd ecommerce-m7
```

### 4.2 Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate     # Windows (PowerShell)
# venv\Scripts\activate.bat # Windows (CMD)
```

### 4.3 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4.4 Configurar variables de entorno (opcional)

Crea un archivo `.env` en la raíz del proyecto (o exporta las variables directamente en tu terminal):

```env
# Django
DJANGO_SECRET_KEY=clave-segura-aqui
DJANGO_DEBUG=True

# Base de datos (solo si usas PostgreSQL)
DATABASE_URL=postgres://usuario:password@localhost:5432/ecommerce_db

# Cloudinary (opcional, solo si usas almacenamiento en la nube)
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

> **Sin `.env` el proyecto funciona igual**: usa SQLite, modo DEBUG=True y almacenamiento local de imágenes.

### 4.5 Configurar la base de datos

#### Desarrollo (SQLite — por defecto)

No requiere configuración adicional. El archivo `db.sqlite3` se crea automáticamente al ejecutar migraciones.

#### Producción (PostgreSQL)

1. Asegúrate de tener PostgreSQL instalado y corriendo.
2. Crea una base de datos:
   ```bash
   createdb ecommerce_db
   ```
3. Define la variable `DATABASE_URL` en tu entorno:
   ```bash
   export DATABASE_URL=postgres://tu_usuario:tu_password@localhost:5432/ecommerce_db
   ```

---

## 5. Ejecución en local

### 5.1 Migraciones

```bash
python manage.py migrate
```

### 5.2 Poblar datos de prueba (opcional)

Este comando crea 6 categorías y 40 productos con imágenes:

```bash
python manage.py poblar_datos
```

### 5.3 Crear superusuario (opcional si ya usaste poblar_datos)

```bash
python manage.py createsuperuser
```
Sigue las instrucciones interactivas para crear un usuario administrador.

### 5.4 Asignar imágenes a productos

```bash
python manage.py arreglar_imagenes
```
Este comando asigna las imágenes locales (en `media/productos/`) a cada producto en la base de datos.

### 5.5 Iniciar servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en: **http://localhost:8000/**

---

## 6. Rutas principales

### Públicas

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/` | `home` | Página principal con carrusel, destacados y novedades |
| `/products/` | `lista_productos` | Catálogo completo con filtros y paginación (12 por página) |
| `/products/<slug>/` | `detalle_producto` | Detalle del producto con galería, precio y relacionados |
| `/categories/` | `lista_categorias` | Cuadrícula de categorías |
| `/categories/<id>/` | `productos_por_categoria` | Productos filtrados por categoría |
| `/search/?q=` | `buscar_productos` | Búsqueda por nombre, descripción y categoría |
| `/cart/` | `ver_carrito` | Carrito de compras con resumen |
| `/cart/add/<id>/` | `agregar_al_carrito` | Agrega un producto al carrito |
| `/cart/update/<id>/` | `actualizar_carrito` | Actualiza la cantidad de un item |
| `/cart/remove/<id>/` | `eliminar_del_carrito` | Elimina un item del carrito |

### Requieren autenticación

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/checkout/` | `checkout` | Formulario de envío y confirmación de compra |
| `/orders/` | `mis_pedidos` | Historial de pedidos del usuario |
| `/orders/<codigo>/` | `detalle_pedido` | Detalle de un pedido específico |
| `/profile/` | `perfil_usuario` | Edición de datos personales y últimos pedidos |
| `/register/` | `registro` | Creación de cuenta de usuario |
| `/accounts/login/` | `login` | Inicio de sesión |
| `/accounts/logout/` | `logout` | Cierre de sesión |

### Solo personal autorizado (staff)

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/products/admin/` | `lista_admin` | Tabla administradora de productos |
| `/products/create/` | `crear_producto` | Formulario para crear un producto |
| `/products/edit/<id>/` | `editar_producto` | Formulario para editar un producto |
| `/products/delete/<id>/` | `eliminar_producto` | Confirmación y eliminación de producto |
| `/admin/` | Django Admin | Panel de administración completo de Django |

---

## 7. Credenciales de prueba

### Administrador (pre-creado)

| Campo | Valor |
|-------|-------|
| Usuario | `admin` |
| Contraseña | `admin123` |
| Tipo | Superusuario (staff) |

### Usuario cliente

No existe un usuario cliente pre-creado. Puedes crearlo de dos formas:

#### Opción A — Desde la interfaz web

1. Abre http://localhost:8000/register/
2. Completa el formulario con:
   - **Nombre de usuario**: `cliente`
   - **Nombre**: `Cliente`
   - **Apellido**: `Prueba`
   - **Email**: `cliente@ejemplo.com`
   - **Contraseña**: `Cliente123!`
   - **Confirmar contraseña**: `Cliente123!`

#### Opción B — Desde la terminal

```bash
python manage.py shell -c "
from django.contrib.auth.models import User
User.objects.create_user('cliente', 'cliente@ejemplo.com', 'Cliente123!')
"
```

---

## 8. Capturas de pantalla

El proyecto no incluye capturas de pantalla predefinidas. Para documentar visualmente la aplicación, se recomienda capturar las siguientes vistas después de ejecutar el proyecto:

| Página | Descripción |
|--------|-------------|
| **Inicio** | Carrusel, productos destacados y novedades |
| **Catálogo** | Cuadrícula de productos con filtros |
| **Detalle de producto** | Imagen, galería, precio, descripción y relacionados |
| **Carrito** | Lista de items con cantidades y total |
| **Checkout** | Formulario de envío |
| **Confirmación de compra** | Detalle del pedido creado |
| **Panel de administración** | Lista de productos en `/products/admin/` |
| **Inicio de sesión** | Formulario de login |

Puedes organizarlas en una carpeta `docs/screenshots/` o `img/` y referenciarlas con Markdown:

```markdown
![Home](img/home.png)
```

---

## 9. Estructura del proyecto

```
ecommerce_m7/
├── build.sh                     # Script de build para Render
├── config/                      # Configuración del proyecto Django
│   ├── settings.py              # Settings con soporte multi-entorno
│   ├── urls.py                  # URLs raíz (admin, auth, media)
│   ├── wsgi.py                  # WSGI para producción
│   └── asgi.py                  # ASGI (no utilizado)
├── manage.py                    # CLI de Django
├── media/                       # Imágenes de productos
│   └── productos/               # 47 archivos de imágenes
├── Procfile                     # Comando web para Render
├── requirements.txt             # Dependencias Python
├── runtime.txt                  # Versión de Python para Render
├── staticfiles/                 # Archivos estáticos compilados
│   └── ...                      # (generado por collectstatic)
└── tienda/                      # Aplicación principal
    ├── admin.py                 # Configuración del admin
    ├── context_processors.py    # Context processors (carrito, categorías)
    ├── forms.py                 # Formularios (Producto, Registro, Perfil, Checkout, Carrito)
    ├── management/commands/     # Comandos personalizados
    │   ├── arreglar_imagenes.py # Asigna imágenes locales a productos
    │   └── poblar_datos.py      # Pobla DB con datos de prueba
    ├── migrations/              # Migraciones de base de datos
    ├── models.py                # Modelos (Categoria, Producto, Carrito, Pedido, etc.)
    ├── static/tienda/css/       # Archivos estáticos
    │   └── style.css            # Estilos personalizados
    ├── templates/               # Plantillas HTML
    │   ├── base.html            # Plantilla base con navbar, footer, messages
    │   ├── home.html            # Página principal
    │   ├── includes/
    │   │   └── product_card.html # Card reutilizable de producto
    │   ├── cart/
    │   │   ├── cart.html        # Vista del carrito
    │   │   └── checkout.html    # Formulario de checkout
    │   ├── orders/
    │   │   ├── detail.html      # Detalle del pedido
    │   │   └── list.html        # Historial de pedidos
    │   ├── products/
    │   │   ├── catalog.html     # Catálogo con filtros
    │   │   ├── categories.html  # Cuadrícula de categorías
    │   │   ├── delete.html      # Confirmación de eliminación
    │   │   ├── detail.html      # Detalle del producto
    │   │   ├── form.html        # Formulario de producto (crear/editar)
    │   │   └── list.html        # Listado admin de productos
    │   └── registration/
    │       ├── login.html       # Inicio de sesión
    │       ├── logged_out.html  # Cierre de sesión
    │       ├── profile.html     # Perfil de usuario
    │       └── register.html    # Registro de usuario
    ├── tests.py                 # Tests unitarios (11 tests)
    ├── urls.py                  # URLs de la aplicación
    └── views.py                 # Vistas (18 vistas)
```

---

## 10. Dependencias

### requirements.txt

```txt
asgiref==3.11.1
Django==6.0.6
pillow==12.3.0
psycopg2-binary==2.9.12
sqlparse==0.5.5
whitenoise==6.12.0
gunicorn==23.0.0
django-cloudinary-storage==0.3.0
dj-database-url==3.1.2
```

> **Nota:** `django-cloudinary-storage` y su dependencia `cloudinary` son **opcionales**. Si no vas a usar Cloudinary, puedes eliminarlos del archivo y descomentar las apps en `INSTALLED_APPS` de `settings.py`. El proyecto funciona correctamente sin ellos usando almacenamiento local.

Para regenerar `requirements.txt` desde cero:

```bash
pip freeze > requirements.txt
```

---

## 11. Revisión general

### Comandos verificados

| Comando | Estado |
|---------|--------|
| `python manage.py migrate` | ✅ Funciona |
| `python manage.py makemigrations` | ✅ Sin cambios pendientes |
| `python manage.py createsuperuser` | ✅ Funciona |
| `python manage.py poblar_datos` | ✅ Crea 6 categorías + 40 productos |
| `python manage.py arreglar_imagenes` | ✅ Asigna imágenes a productos |
| `python manage.py test tienda` | ✅ 11 tests OK |
| `python manage.py runserver` | ✅ Sirve en http://localhost:8000/ |
| `gunicorn config.wsgi` | ✅ (producción) |

### Validación de rutas

Todas las rutas documentadas en la sección 6 fueron verificadas contra `tienda/urls.py` y `config/urls.py`. Cada URL name tiene su template y vista correspondiente.

### Datos precargados

- **Categorías**: 6 (Electrónica, Computación, Celulares, Audio, Gaming, Oficina)
- **Productos**: 40 con imágenes, precios, descuentos y stock
- **Usuario admin**: `admin` / `admin123` (superusuario con acceso a todo)

### Despliegue en Render

El proyecto incluye configuración lista para [Render](https://render.com):

- `Procfile` → `web: gunicorn config.wsgi`
- `runtime.txt` → `python-3.12.1`
- `build.sh` → instala dependencias, migra, copia media y asigna imágenes

**Variables de entorno requeridas en Render:**

| Variable | Descripción |
|----------|-------------|
| `DJANGO_SECRET_KEY` | Clave secreta de Django (generar con `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`) |
| `DJANGO_DEBUG` | `False` en producción |
| `DATABASE_URL` | URL de conexión PostgreSQL (Render la provee automáticamente) |
| `MEDIA_ROOT` | Ruta al Persistent Disk (ej: `/var/data/media`) |

---

## Licencia

Proyecto educativo de portafolio. Código libre para fines de aprendizaje y demostración.
