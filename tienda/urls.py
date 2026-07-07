from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.lista_productos, name="lista_productos"),
    # Admin CRUD routes (must be BEFORE slug route)
    path(
        "products/admin/",
        views.lista_admin,
        name="lista_admin",
    ),
    path(
        "products/create/",
        views.crear_producto,
        name="crear_producto",
    ),
    path(
        "products/edit/<int:id>/",
        views.editar_producto,
        name="editar_producto",
    ),
    path(
        "products/delete/<int:id>/",
        views.eliminar_producto,
        name="eliminar_producto",
    ),
    path(
        "products/<slug:slug>/",
        views.detalle_producto,
        name="detalle_producto",
    ),
    path("categories/", views.lista_categorias, name="lista_categorias"),
    path(
        "categories/<int:categoria_id>/",
        views.productos_por_categoria,
        name="productos_por_categoria",
    ),
    path("search/", views.buscar_productos, name="buscar_productos"),
    path("cart/", views.ver_carrito, name="ver_carrito"),
    path(
        "cart/add/<int:producto_id>/",
        views.agregar_al_carrito,
        name="agregar_al_carrito",
    ),
    path(
        "cart/update/<int:item_id>/",
        views.actualizar_carrito,
        name="actualizar_carrito",
    ),
    path(
        "cart/remove/<int:item_id>/",
        views.eliminar_del_carrito,
        name="eliminar_del_carrito",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.mis_pedidos, name="mis_pedidos"),
    path(
        "orders/<str:codigo>/",
        views.detalle_pedido,
        name="detalle_pedido",
    ),
    path("register/", views.registro, name="registro"),
    path("profile/", views.perfil_usuario, name="perfil_usuario"),
]
