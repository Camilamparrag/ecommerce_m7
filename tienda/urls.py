from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_productos, name="lista_productos"),
    path("create/", views.crear_producto, name="crear_producto"),
    path("edit/<int:id>/", views.editar_producto, name="editar_producto"),
    path("delete/<int:id>/", views.eliminar_producto, name="eliminar_producto"),
]
