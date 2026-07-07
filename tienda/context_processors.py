from .models import Categoria, Carrito


def carrito_info(request):
    cart_count = 0
    cart_total = 0
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            cart_count = carrito.cantidad
            cart_total = carrito.total
        except Carrito.DoesNotExist:
            pass
    elif request.session.session_key:
        try:
            carrito = Carrito.objects.get(
                session_key=request.session.session_key
            )
            cart_count = carrito.cantidad
            cart_total = carrito.total
        except Carrito.DoesNotExist:
            pass

    return {
        "carrito_count": cart_count,
        "carrito_total": cart_total,
    }


def categorias_globales(request):
    return {
        "categorias_nav": Categoria.objects.filter(activa=True),
    }
