# E-Commerce M7

Plataforma eCommerce profesional construida con Django 6 + Bootstrap 5. Catálogo de productos, carrito de compras, checkout, pedidos, autenticación y panel administrador.

## Características

- **Catálogo**: productos con imágenes, categorías, precios, stock, descuentos
- **Buscador**: búsqueda por nombre, descripción, categoría
- **Filtros**: por categoría, rango de precio, disponibilidad, orden
- **Carrito híbrido**: sesión para anónimos, base de datos para autenticados
- **Checkout**: formulario de envío, confirmación, descuento de stock
- **Pedidos**: historial completo con estados, detalles, items
- **Autenticación**: registro, login/logout, perfil de usuario
- **Admin**: CRUD completo para staff, panel Django Admin mejorado
- **UI/UX**: Bootstrap 5, Bootstrap Icons, animaciones, breadcrumbs, responsive
- **Admin creado**: `admin` / `admin123`
- **Datos de prueba**: 6 categorías, 35 productos

## Stack

| Componente | Tecnología |
|------------|-----------|
| Backend | Django 6.0.6 |
| Frontend | Bootstrap 5.3.3 + Bootstrap Icons |
| Base de datos | SQLite (dev) / PostgreSQL (prod vía `DATABASE_URL`) |
| Imágenes | Pillow 12.3.0, `ImageField` |
| Auth | Django `django.contrib.auth` |

## Modelos

### Categoria
| Campo | Tipo |
|-------|------|
| nombre | CharField(100), único |
| descripcion | TextField, opcional |
| imagen | ImageField, opcional |
| activa | BooleanField, default=True |

### Producto
| Campo | Tipo |
|-------|------|
| nombre | CharField(100) |
| slug | SlugField, único, auto-generado |
| descripcion_corta | CharField(200), opcional |
| descripcion | TextField |
| precio | DecimalField(10,2) |
| descuento | DecimalField(5,2), default=0 |
| stock | PositiveIntegerField, default=0 |
| categoria | ForeignKey → Categoria |
| imagen | ImageField, opcional |
| fecha_creacion | DateTimeField, auto |
| activo | BooleanField, default=True |
| destacado | BooleanField, default=False |

Propiedades: `precio_final`, `tiene_descuento`, `disponible`

### ImagenProducto
| Campo | Tipo |
|-------|------|
| producto | ForeignKey(related_name="imagenes") |
| imagen | ImageField |
| orden | PositiveIntegerField, default=0 |

### Carrito
| Campo | Tipo |
|-------|------|
| usuario | OneToOneField(User, null) |
| session_key | CharField(40, null, unique) |
| fecha_creacion | DateTimeField, auto |
| fecha_actualizacion | DateTimeField, auto |

Propiedades: `total`, `cantidad`

### ItemCarrito
| Campo | Tipo |
|-------|------|
| carrito | ForeignKey(related_name="items") |
| producto | ForeignKey → Producto |
| cantidad | PositiveIntegerField, default=1 |
| precio_unitario | DecimalField(10,2) |

Propiedad: `subtotal`

### Pedido
| Campo | Tipo |
|-------|------|
| codigo | CharField(20), único, auto-generado |
| usuario | ForeignKey → User |
| nombre | CharField(100) |
| direccion | CharField(200) |
| ciudad | CharField(100) |
| telefono | CharField(20) |
| email | EmailField |
| notas | TextField, opcional |
| total | DecimalField(12,2) |
| estado | CharField (choices: pendiente, preparacion, enviado, entregado, cancelado) |
| fecha | DateTimeField, auto |

### ItemPedido
| Campo | Tipo |
|-------|------|
| pedido | ForeignKey(related_name="items") |
| producto | ForeignKey → Producto (null on delete) |
| nombre_producto | CharField(100) |
| cantidad | PositiveIntegerField |
| precio_unitario | DecimalField(10,2) |
| subtotal | DecimalField(12,2) |

## Rutas

### Públicas
| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/` | home | Hero, destacados, categorías, nuevos |
| `/products/` | lista_productos | Catálogo con filtros y paginación |
| `/products/<slug>/` | detalle_producto | Galería, precio, stock, relacionados |
| `/categories/` | lista_categorias | Grid de categorías |
| `/categories/<id>/` | productos_por_categoria | Productos filtrados por categoría |
| `/search/?q=` | buscar_productos | Búsqueda por texto |
| `/cart/` | ver_carrito | Tabla de items, resumen |
| `/cart/add/<id>/` | agregar_al_carrito | Agregar producto |
| `/cart/update/<id>/` | actualizar_carrito | Cambiar cantidad |
| `/cart/remove/<id>/` | eliminar_del_carrito | Quitar producto |

### Requieren autenticación
| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/checkout/` | checkout | Formulario de envío + resumen |
| `/orders/` | mis_pedidos | Historial de pedidos |
| `/orders/<codigo>/` | detalle_pedido | Detalle del pedido |
| `/profile/` | perfil_usuario | Editar datos personales |
| `/register/` | registro | Crear cuenta |
| `/accounts/login/` | login | Iniciar sesión |
| `/accounts/logout/` | logout | Cerrar sesión |

### Staff-only
| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/products/admin/` | lista_admin | Tabla admin con todos los productos |
| `/products/create/` | crear_producto | Formulario de creación |
| `/products/edit/<id>/` | editar_producto | Formulario de edición |
| `/products/delete/<id>/` | eliminar_producto | Confirmación de eliminación |
| `/admin/` | Django Admin | Panel de administración completo |

## Instalación

```bash
# 1. Clonar
git clone <repo-url>
cd ecommerce_m7

# 2. Entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Migraciones
python manage.py migrate

# 5. Poblar datos de prueba (opcional)
python manage.py poblar_datos

# 6. Crear superusuario (opcional)
python manage.py createsuperuser

# 7. Iniciar
python manage.py runserver
```

Abrir http://localhost:8000/

### Usuario admin pre-creado
- **Usuario**: `admin`
- **Contraseña**: `admin123`

## Variable de entorno

Crear archivo `.env` en la raíz:

```env
DJANGO_SECRET_KEY=clave-secreta-segura
DJANGO_DEBUG=False
DATABASE_URL=postgres://usuario:password@localhost:5432/ecommerce_db
```

Sin `.env`, el proyecto funciona con SQLite y valores por defecto seguros para desarrollo.

## Screenshots

| Página | Vista |
|--------|-------|
| Home | ![Home](img/ecommerce_home.png) |
| Catálogo | ![Catálogo](img/ecommerce_catalogo.png) |
| Detalle | ![Detalle](img/ecommerce_detalle.png) |
| Carrito | ![Carrito](img/ecommerce_carrito.png) |
| Checkout | ![Checkout](img/ecommerce_checkout.png) |
| Pedidos | ![Pedidos](img/ecommerce_pedidos.png) |

## Licencia

Proyecto educativo de portafolio.
