from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Categoria, Producto, Carrito, ItemCarrito, Pedido


class ProductoModelTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Test", descripcion="Cat")
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción",
            precio=10000,
            stock=10,
            categoria=self.categoria,
        )

    def test_precio_final_sin_descuento(self):
        self.assertEqual(self.producto.precio_final, 10000)

    def test_precio_final_con_descuento(self):
        self.producto.descuento = 20
        self.assertEqual(self.producto.precio_final, 8000)

    def test_disponible_con_stock_y_activo(self):
        self.assertTrue(self.producto.disponible)

    def test_no_disponible_sin_stock(self):
        self.producto.stock = 0
        self.assertFalse(self.producto.disponible)

    def test_slug_auto_generado(self):
        self.assertEqual(self.producto.slug, "producto-test")


class CarritoModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.categoria = Categoria.objects.create(nombre="Test")
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Desc",
            precio=5000,
            stock=5,
            categoria=self.categoria,
        )
        self.carrito = Carrito.objects.create(usuario=self.user)
        self.item = ItemCarrito.objects.create(
            carrito=self.carrito,
            producto=self.producto,
            cantidad=2,
            precio_unitario=5000,
        )

    def test_item_subtotal(self):
        self.assertEqual(self.item.subtotal, 10000)

    def test_carrito_total(self):
        self.assertEqual(self.carrito.total, 10000)

    def test_carrito_cantidad(self):
        self.assertEqual(self.carrito.cantidad, 2)


class CheckoutFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="comprador", password="pass123")
        self.categoria = Categoria.objects.create(nombre="Test")
        self.producto = Producto.objects.create(
            nombre="Prod Checkout",
            descripcion="Test",
            precio=10000,
            stock=3,
            categoria=self.categoria,
        )

    def test_checkout_requiere_autenticacion(self):
        response = self.client.get(reverse("checkout"))
        self.assertNotEqual(response.status_code, 200)

    def test_checkout_reduce_stock(self):
        self.client.login(username="comprador", password="pass123")
        carrito = Carrito.objects.create(usuario=self.user)
        ItemCarrito.objects.create(
            carrito=carrito,
            producto=self.producto,
            cantidad=2,
            precio_unitario=10000,
        )
        response = self.client.post(
            reverse("checkout"),
            {
                "nombre": "Juan",
                "direccion": "Calle 123",
                "ciudad": "Santiago",
                "telefono": "912345678",
                "email": "juan@test.com",
            },
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 1)
        self.assertEqual(Pedido.objects.count(), 1)

    def test_registro_usuario(self):
        response = self.client.post(
            reverse("registro"),
            {
                "username": "nuevo",
                "first_name": "Nuevo",
                "last_name": "User",
                "email": "nuevo@test.com",
                "password1": "Password123!",
                "password2": "Password123!",
            },
        )
        self.assertEqual(User.objects.filter(username="nuevo").count(), 1)
