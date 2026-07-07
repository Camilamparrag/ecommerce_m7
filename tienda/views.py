from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.db.models import Q
from django.core.paginator import Paginator
from .models import (
    Categoria,
    Producto,
    ImagenProducto,
    Carrito,
    ItemCarrito,
    Pedido,
    ItemPedido,
)
from .forms import (
    ProductoForm,
    RegistroForm,
    PerfilForm,
    CheckoutForm,
    CarritoForm,
)

# ─── HELPERS ────────────────────────────────────────


def obtener_carrito(request):
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        carrito, _ = Carrito.objects.get_or_create(
            session_key=request.session.session_key
        )
    return carrito


# ─── HOME ───────────────────────────────────────────


def home(request):
    destacados = Producto.objects.filter(
        activo=True, destacado=True
    ).select_related("categoria")[:8]
    nuevos = Producto.objects.filter(activo=True).select_related("categoria")[:8]
    return render(
        request,
        "home.html",
        {
            "destacados": destacados,
            "nuevos": nuevos,
        },
    )


# ─── PRODUCTOS ──────────────────────────────────────


def lista_productos(request):
    productos = Producto.objects.filter(activo=True).select_related("categoria")
    categorias = Categoria.objects.filter(activa=True)

    categoria_id = request.GET.get("categoria")
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    precio_min = request.GET.get("precio_min")
    precio_max = request.GET.get("precio_max")
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)

    disponible = request.GET.get("disponible")
    if disponible:
        productos = productos.filter(stock__gt=0)

    orden = request.GET.get("orden", "nombre")
    if orden == "precio":
        productos = productos.order_by("precio")
    elif orden == "-precio":
        productos = productos.order_by("-precio")
    elif orden == "-fecha_creacion":
        productos = productos.order_by("-fecha_creacion")
    else:
        productos = productos.order_by("nombre")

    paginator = Paginator(productos, 12)
    page = request.GET.get("page")
    productos_page = paginator.get_page(page)

    return render(
        request,
        "products/catalog.html",
        {
            "productos": productos_page,
            "categorias": categorias,
            "filtro_categoria": int(categoria_id) if categoria_id else None,
            "precio_min": precio_min,
            "precio_max": precio_max,
            "disponible": disponible,
            "orden": orden,
        },
    )


def detalle_producto(request, slug):
    producto = get_object_or_404(
        Producto.objects.select_related("categoria"), slug=slug, activo=True
    )
    imagenes = producto.imagenes.all()
    relacionados = Producto.objects.filter(
        categoria=producto.categoria, activo=True
    ).exclude(id=producto.id)[:4]
    return render(
        request,
        "products/detail.html",
        {
            "producto": producto,
            "imagenes": imagenes,
            "relacionados": relacionados,
        },
    )


def lista_categorias(request):
    categorias = Categoria.objects.filter(activa=True)
    return render(request, "products/categories.html", {"categorias": categorias})


def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, activa=True)
    productos = Producto.objects.filter(
        categoria=categoria, activo=True
    ).select_related("categoria")
    paginator = Paginator(productos, 12)
    page = request.GET.get("page")
    productos_page = paginator.get_page(page)
    return render(
        request,
        "products/catalog.html",
        {
            "productos": productos_page,
            "categoria_actual": categoria,
            "categorias": Categoria.objects.filter(activa=True),
        },
    )


def buscar_productos(request):
    q = request.GET.get("q", "").strip()
    productos = Producto.objects.filter(activo=True).select_related("categoria")
    if q:
        productos = productos.filter(
            Q(nombre__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(descripcion_corta__icontains=q)
            | Q(categoria__nombre__icontains=q)
        )
    else:
        productos = productos.none()
    paginator = Paginator(productos, 12)
    page = request.GET.get("page")
    productos_page = paginator.get_page(page)
    return render(
        request,
        "products/catalog.html",
        {
            "productos": productos_page,
            "query": q,
            "categorias": Categoria.objects.filter(activa=True),
        },
    )


# ─── CARRITO ────────────────────────────────────────


def ver_carrito(request):
    carrito = obtener_carrito(request)
    items = carrito.items.select_related("producto__categoria").all()
    return render(request, "cart/cart.html", {"carrito": carrito, "items": items})


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    if not producto.disponible:
        messages.error(request, "Este producto no está disponible.")
        return redirect("detalle_producto", slug=producto.slug)

    carrito = obtener_carrito(request)
    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={"cantidad": 1, "precio_unitario": producto.precio_final},
    )
    if not created:
        if item.cantidad >= producto.stock:
            messages.warning(
                request, f"Solo hay {producto.stock} unidades disponibles."
            )
        else:
            item.cantidad += 1
            item.save()
            messages.success(request, f"{producto.nombre} agregado al carrito.")
    else:
        messages.success(request, f"{producto.nombre} agregado al carrito.")

    return redirect(request.META.get("HTTP_REFERER", "ver_carrito"))


def actualizar_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    carrito = obtener_carrito(request)
    if item.carrito != carrito:
        messages.error(request, "Este item no pertenece a tu carrito.")
        return redirect("ver_carrito")

    if request.method == "POST":
        form = CarritoForm(request.POST, instance=item, producto=item.producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Carrito actualizado.")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return redirect("ver_carrito")


def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    carrito = obtener_carrito(request)
    if item.carrito == carrito:
        item.delete()
        messages.success(request, "Producto eliminado del carrito.")
    return redirect("ver_carrito")


# ─── CHECKOUT ───────────────────────────────────────


@login_required
def checkout(request):
    carrito = obtener_carrito(request)
    items = carrito.items.select_related("producto").all()
    if not items:
        messages.info(request, "Tu carrito está vacío.")
        return redirect("lista_productos")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.total = carrito.total
            pedido.save()
            for item in items:
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    nombre_producto=item.producto.nombre,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario,
                    subtotal=item.subtotal,
                )
                producto = item.producto
                producto.stock -= item.cantidad
                producto.save()
            items.delete()
            messages.success(
                request,
                f"Pedido {pedido.codigo} confirmado correctamente.",
            )
            return redirect("detalle_pedido", codigo=pedido.codigo)
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        initial = {
            "nombre": f"{request.user.first_name} {request.user.last_name}".strip()
            or request.user.username,
            "email": request.user.email,
        }
        form = CheckoutForm(initial=initial)

    return render(
        request,
        "cart/checkout.html",
        {"form": form, "carrito": carrito, "items": items},
    )


# ─── PEDIDOS ────────────────────────────────────────


@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).prefetch_related("items")
    return render(request, "orders/list.html", {"pedidos": pedidos})


@login_required
def detalle_pedido(request, codigo):
    pedido = get_object_or_404(
        Pedido.objects.prefetch_related("items"),
        codigo=codigo,
        usuario=request.user,
    )
    return render(request, "orders/detail.html", {"pedido": pedido})


# ─── USUARIOS ───────────────────────────────────────


def registro(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = RegistroForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def perfil_usuario(request):
    pedidos = Pedido.objects.filter(usuario=request.user)[:5]
    if request.method == "POST":
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("perfil_usuario")
        else:
            messages.error(request, "Corrige los errores.")
    else:
        form = PerfilForm(instance=request.user)
    return render(
        request,
        "registration/profile.html",
        {"form": form, "pedidos": pedidos},
    )


# ─── ADMIN CRUD (staff-only) ─────────────────────────

staff_required = user_passes_test(lambda u: u.is_staff)


@staff_required
def lista_admin(request):
    productos = Producto.objects.all().select_related("categoria")
    return render(request, "products/list.html", {"productos": productos})


@staff_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect("lista_admin")
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = ProductoForm()
    return render(
        request,
        "products/form.html",
        {"form": form, "titulo": "Nuevo Producto"},
    )


@staff_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("lista_admin")
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = ProductoForm(instance=producto)
    return render(
        request,
        "products/form.html",
        {"form": form, "titulo": "Editar Producto"},
    )


@staff_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("lista_admin")
    return render(request, "products/delete.html", {"producto": producto})
