from django.contrib import admin
from django.db.models import Count
from .models import Categoria, Producto, ImagenProducto, Carrito, ItemCarrito, Pedido, ItemPedido


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    readonly_fields = ["producto", "nombre_producto", "cantidad", "precio_unitario", "subtotal"]
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    readonly_fields = ["producto", "cantidad", "precio_unitario", "subtotal"]
    extra = 0


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "activa", "producto_count"]
    search_fields = ["nombre"]
    list_filter = ["activa"]
    ordering = ["nombre"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_producto_count=Count("productos"))

    def producto_count(self, obj):
        return obj._producto_count

    producto_count.admin_order_field = "_producto_count"
    producto_count.short_description = "Productos"


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "nombre",
        "categoria",
        "precio",
        "precio_final",
        "stock",
        "destacado",
        "activo",
    ]
    search_fields = ["nombre", "descripcion"]
    list_filter = ["categoria", "activo", "destacado"]
    list_editable = ["precio", "stock", "activo", "destacado"]
    list_per_page = 25
    ordering = ["-fecha_creacion"]
    date_hierarchy = "fecha_creacion"
    prepopulated_fields = {"slug": ("nombre",)}
    inlines = [ImagenProductoInline]


@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = ["id", "producto", "orden"]
    list_editable = ["orden"]


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ["id", "usuario", "session_key", "items_qty", "items_total", "fecha_actualizacion"]
    inlines = [ItemCarritoInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("items")

    def items_qty(self, obj):
        return sum(i.cantidad for i in obj.items.all())

    def items_total(self, obj):
        return sum(i.subtotal for i in obj.items.all())

    items_qty.short_description = "Cantidad"
    items_total.short_description = "Total"


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["codigo", "usuario", "total", "estado", "fecha"]
    list_filter = ["estado", "fecha"]
    search_fields = ["codigo", "usuario__username", "nombre"]
    list_editable = ["estado"]
    readonly_fields = ["codigo", "fecha", "total"]
    inlines = [ItemPedidoInline]
    ordering = ["-fecha"]
    date_hierarchy = "fecha"
