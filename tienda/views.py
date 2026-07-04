from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto, Categoria
from .forms import ProductoForm


def lista_productos(request):
    productos = Producto.objects.all().order_by("nombre")
    return render(request, "products/list.html", {"productos": productos})


def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect("lista_productos")
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = ProductoForm()
    return render(request, "products/form.html", {"form": form, "titulo": "Nuevo Producto"})


def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("lista_productos")
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "products/form.html", {"form": form, "titulo": "Editar Producto"})


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("lista_productos")
    return render(request, "products/delete.html", {"producto": producto})
