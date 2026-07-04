from django.core.management.base import BaseCommand
from tienda.models import Categoria, Producto
from decimal import Decimal


class Command(BaseCommand):
    help = 'Pobla la base de datos con categorías y productos de prueba'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando creación de categorías...")

        nombres_categorias = [
            "Electrónica",
            "Computación",
            "Celulares",
            "Audio",
            "Gaming",
            "Oficina"
        ]

        categorias_creadas = 0
        for nombre in nombres_categorias:
            categoria, creada = Categoria.objects.get_or_create(nombre=nombre)
            if creada:
                categorias_creadas += 1
                self.stdout.write(f"  ✓ Categoría creada: {nombre}")
            else:
                self.stdout.write(f"  - Categoría ya existe: {nombre}")

        self.stdout.write(f"\nTotal de categorías creadas: {categorias_creadas}")

        productos_existentes = Producto.objects.count()
        self.stdout.write(f"\nProductos existentes: {productos_existentes}")

        productos_por_categorias = {
            "Electrónica": [
                {"nombre": "Notebook Lenovo IdeaPad 5", "descripcion": "Laptop con procesador Intel i5, 8GB RAM, 512GB SSD", "precio": 1299999, "stock": 25},
                {"nombre": "Mouse Logitech G203", "descripcion": "Mouse para juegos con 8 botones, iluminación RGB", "precio": 45000, "stock": 50},
                {"nombre": "Monitor Samsung 27\"", "descripcion": "Monitor LED Full HD de 27 pulgadas", "precio": 890000, "stock": 15},
                {"nombre": "Teclado Mecánico Redragon", "descripcion": "Teclado mecánico retroiluminado RGB, switches verdes", "precio": 120000, "stock": 30},
                {"nombre": "SSD Kingston 1TB", "descripcion": "Unidad de estado sólido NVMe, 1TB, lectura 3500MB/s", "precio": 450000, "stock": 40},
                {"nombre": "Memoria RAM Corsair 16GB", "descripcion": "Kit de memoria DDR4, 16GB, 3000MHz", "precio": 220000, "stock": 35},
                {"nombre": "Audífonos Sony WH-CH520", "descripcion": "Audífonos inalámbricos con cancelación de ruido", "precio": 180000, "stock": 20},
                {"nombre": "Parlante JBL Flip", "descripcion": "Bocina portátil con sonido potente y resistente al agua", "precio": 150000, "stock": 45},
                {"nombre": "Webcam Logitech C920", "descripcion": "Cámara web con resolución Full HD 1080p", "precio": 120000, "stock": 30},
                {"nombre": "Impresora HP Smart Tank", "descripcion": "Impresora multifuncional con sistema de tinta recargable", "precio": 380000, "stock": 15},
            ],
            "Computación": [
                {"nombre": "Procesador Intel i7 12 generación", "descripcion": "Procesador de 8 núcleos, 16GB de caché", "precio": 850000, "stock": 20},
                {"nombre": "Tarjeta gráfica NVIDIA RTX 3060", "descripcion": "8GB GDDR6, para gaming y tareas de GPU", "precio": 1500000, "stock": 25},
                {"nombre": "Disco duro Western Digital 4TB", "descripcion": "HDD de 3.5", "precio": 280000, "stock": 40},
                {"nombre": "Fuente de poder Corsair 750W", "descripcion": "Fuente de poder modular 80+ Gold", "precio": 200000, "stock": 30},
                {"nombre": "Caja PC Cooler Master", "descripcion": "Gabinete ATX con iluminación RGB", "precio": 180000, "stock": 35},
            ],
            "Celulares": [
                {"nombre": "iPhone 15 Pro", "descripcion": "Teléfono móvil Apple con cámara triple", "precio": 2500000, "stock": 20},
                {"nombre": "Samsung Galaxy S24 Ultra", "descripcion": "Teléfono móvil Android con cámara de 200MP", "precio": 2700000, "stock": 15},
                {"nombre": "Xiaomi Mi 13", "descripcion": "Teléfono móvil con pantalla AMOLED 120Hz", "precio": 1800000, "stock": 30},
                {"nombre": "OnePlus 12", "descripcion": "Teléfono móvil con batería de 5000mAh", "precio": 1600000, "stock": 25},
                {"nombre": "Realme GT 6", "descripcion": "Teléfono móvil con procesador Snapdragon 8+", "precio": 1400000, "stock": 28},
            ],
            "Audio": [
                {"nombre": "Auriculares Bose QuietComfort 45", "descripcion": "Auriculares inalámbricos con cancelación de ruido", "precio": 850000, "stock": 20},
                {"nombre": "Altavoz Sonos One", "descripcion": "Altavoz inteligente con sonido envolvente", "precio": 450000, "stock": 25},
                {"nombre": "Microphone Boya Y515", "descripcion": "Microfono USB para grabación de audio", "precio": 150000, "stock": 35},
                {"nombre": "Equalizador Behringer DCX2496", "descripcion": "Procesador de señal digital de 6 bandas", "precio": 280000, "stock": 15},
                {"nombre": "Auriculares con cable Sony MDR-XB55AP", "descripcion": "Auriculares deportivos con sonido extra bass", "precio": 80000, "stock": 50},
            ],
            "Gaming": [
                {"nombre": "PlayStation 5", "descripcion": "Consola de videojuegos Sony con SSD 825GB", "precio": 2000000, "stock": 20},
                {"nombre": "Xbox Series X", "descripcion": "Consola de videojuegos Microsoft con 120FPS", "precio": 1900000, "stock": 25},
                {"nombre": "Nintendo Switch OLED", "descripcion": "Consola portátil con pantalla OLED", "precio": 900000, "stock": 35},
                {"nombre": "Joystick Xbox Series X", "descripcion": "Mando inalámbrico con vibración", "precio": 120000, "stock": 60},
                {"nombre": "Raton para juegos Razer Kiyo", "descripcion": "Mause con sensor óptico de 16000 DPI", "precio": 150000, "stock": 45},
            ],
            "Oficina": [
                {"nombre": "Escritorio de oficina IKEA", "descripcion": "Mesa para ordenador de madera", "precio": 450000, "stock": 10},
                {"nombre": "Silla ejecutiva Mr. Dork", "descripcion": "Silla de oficina con respaldo alto", "precio": 650000, "stock": 15},
                {"nombre": "Impresora láser HP LaserJet Pro", "descripcion": "Impresora láser monocromática", "precio": 380000, "stock": 20},
                {"nombre": "Escáner Epson 2200", "descripcion": "Escáner de sobremesa A4", "precio": 280000, "stock": 25},
                {"nombre": "Estantería de archivos metálica", "descripcion": "Estantería archivadora metálica", "precio": 180000, "stock": 30},
            ],
        }

        produtos_creados = 0
        self.stdout.write("\nCreando productos...")

        for nombre_categoria, productos_data in productos_por_categorias.items():
            self.stdout.write(f"\nCategoría: {nombre_categoria}")
            categoria = Categoria.objects.get(nombre=nombre_categoria)

            for prod in productos_data:
                nombre_producto = prod["nombre"]
                categoria_producto = categoria

                precio_decimal = Decimal(str(prod["precio"]))

                nuevo_producto, creado = Producto.objects.get_or_create(
                    nombre=nombre_producto,
                    categoria=categoria_producto,
                    defaults={
                        "descripcion": prod["descripcion"],
                        "precio": precio_decimal,
                        "stock": prod["stock"],
                        "activo": True,
                    }
                )

                if creado:
                    produtos_creados += 1
                    self.stdout.write(f"  ✓ {nombre_producto}")
                else:
                    self.stdout.write(f"  - {nombre_producto} (ya existe)")

        self.stdout.write(f"\n✓ {produtos_creados} productos creados")
        self.stdout.write(f"✓ {categorias_creadas} categorías creadas\n")

        self.stdout.write("\n✓ La base de datos se ha poblado correctamente!")
        self.stdout.write("Catálogo disponible en: /productos/")
