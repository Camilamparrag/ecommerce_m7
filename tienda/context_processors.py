from django.db.models import Sum, Count
from .models import Categoria, Carrito


def carrito_info(request):
    cart_count = 0
    cart_total = 0
    if request.user.is_authenticated:
        carrito_qs = Carrito.objects.filter(usuario=request.user).prefetch_related("items")
    elif request.session.session_key:
        carrito_qs = Carrito.objects.filter(
            session_key=request.session.session_key
        ).prefetch_related("items")
    else:
        carrito_qs = Carrito.objects.none()

    for carrito in carrito_qs:
        items = list(carrito.items.all())
        cart_count = sum(i.cantidad for i in items)
        cart_total = sum(i.subtotal for i in items)

    return {
        "carrito_count": cart_count,
        "carrito_total": cart_total,
    }


def categorias_globales(request):
    return {
        "categorias_nav": Categoria.objects.filter(activa=True),
    }
