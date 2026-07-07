from django.core.management.base import BaseCommand
from tienda.models import Categoria, Producto
from decimal import Decimal


class Command(BaseCommand):
    help = "Pobla la base de datos con categorías y productos de prueba"

    def handle(self, *args, **options):
        self.stdout.write("=== Poblando Base de Datos ===\n")

        categorias_creadas = 0
        nombres_categorias = [
            "Electrónica",
            "Computación",
            "Celulares",
            "Audio",
            "Gaming",
            "Oficina",
        ]
        self.stdout.write("Creando categorías...")
        for nombre in nombres_categorias:
            cat, creada = Categoria.objects.get_or_create(
                nombre=nombre, defaults={"activa": True}
            )
            if creada:
                categorias_creadas += 1
                self.stdout.write(f"  ✓ {nombre}")
            else:
                self.stdout.write(f"  - {nombre} (ya existe)")

        self.stdout.write(f"\nCategorías creadas: {categorias_creadas}\n")

        data = {
            "Electrónica": [
                {
                    "nombre": "Notebook Lenovo IdeaPad 5",
                    "descripcion_corta": "Laptop i5 8GB RAM 512GB SSD",
                    "descripcion": "Laptop con procesador Intel i5 de 12ª generación, 8GB RAM DDR4, 512GB SSD NVMe.",
                    "precio": 1299999,
                    "descuento": 10,
                    "stock": 25,
                },
                {
                    "nombre": "Mouse Logitech G203",
                    "descripcion_corta": "Mouse gaming 8000 DPI RGB",
                    "descripcion": "Mouse para juegos con sensor óptico de 8000 DPI, iluminación RGB personalizable.",
                    "precio": 45000,
                    "stock": 50,
                },
                {
                    "nombre": "Monitor Samsung 27\"",
                    "descripcion_corta": "Monitor IPS Full HD 75Hz",
                    "descripcion": "Monitor LED IPS de 27 pulgadas, resolución Full HD, 75Hz, HDMI y VGA.",
                    "precio": 890000,
                    "descuento": 5,
                    "stock": 15,
                },
                {
                    "nombre": "Teclado Mecánico Redragon",
                    "descripcion_corta": "Teclado RGB switches Outemu",
                    "descripcion": "Teclado mecánico retroiluminado RGB, switches Outemu Blue, 104 teclas.",
                    "precio": 120000,
                    "descuento": 15,
                    "stock": 30,
                },
                {
                    "nombre": "SSD Kingston 1TB",
                    "descripcion_corta": "SSD NVMe 1TB 3500MB/s",
                    "descripcion": "Unidad de estado sólido NVMe M.2, 1TB, lectura 3500MB/s, escritura 2800MB/s.",
                    "precio": 450000,
                    "stock": 40,
                },
                {
                    "nombre": "Memoria RAM Corsair 16GB",
                    "descripcion_corta": "Kit DDR4 16GB 3200MHz",
                    "descripcion": "Kit de memoria RAM DDR4, 2x8GB, 3200MHz, con disipador de calor.",
                    "precio": 220000,
                    "stock": 35,
                },
                {
                    "nombre": "Audífonos Sony WH-CH520",
                    "descripcion_corta": "Audífonos inalámbricos Bluetooth",
                    "descripcion": "Audífonos inalámbricos con cancelación de ruido, batería 50h, USB-C.",
                    "precio": 180000,
                    "descuento": 10,
                    "stock": 20,
                },
                {
                    "nombre": "Parlante JBL Flip",
                    "descripcion_corta": "Bocina portátil resistente al agua",
                    "descripcion": "Bocina Bluetooth portátil con sonido potente, resistente al agua IPX7.",
                    "precio": 150000,
                    "stock": 45,
                },
                {
                    "nombre": "Webcam Logitech C920",
                    "descripcion_corta": "Cámara web Full HD 1080p",
                    "descripcion": "Cámara web con resolución Full HD 1080p, micrófono estéreo integrado.",
                    "precio": 120000,
                    "stock": 30,
                },
                {
                    "nombre": "Impresora HP Smart Tank",
                    "descripcion_corta": "Impresora multifuncional WiFi",
                    "descripcion": "Impresora multifuncional con sistema de tinta recargable, WiFi y Bluetooth.",
                    "precio": 380000,
                    "stock": 15,
                },
            ],
            "Computación": [
                {
                    "nombre": "Procesador Intel i7 12ª Gen",
                    "descripcion_corta": "CPU 8 núcleos 16 hilos",
                    "descripcion": "Procesador Intel Core i7-12700K, 8 núcleos de rendimiento, 4.9GHz turbo.",
                    "precio": 850000,
                    "stock": 20,
                },
                {
                    "nombre": "Tarjeta Gráfica RTX 3060",
                    "descripcion_corta": "NVIDIA RTX 3060 12GB GDDR6",
                    "descripcion": "Tarjeta gráfica NVIDIA GeForce RTX 3060, 12GB GDDR6, Ray Tracing.",
                    "precio": 1500000,
                    "descuento": 5,
                    "stock": 25,
                },
                {
                    "nombre": "Disco Duro WD 4TB",
                    "descripcion_corta": "HDD 3.5\" 5400RPM",
                    "descripcion": "Disco duro Western Digital de 4TB, 3.5 pulgadas, 5400RPM, SATA III.",
                    "precio": 280000,
                    "stock": 40,
                },
                {
                    "nombre": "Fuente Poder Corsair 750W",
                    "descripcion_corta": "PSU modular 80+ Gold",
                    "descripcion": "Fuente de poder Corsair RM750x, modular, 80+ Gold, ventilador de 135mm.",
                    "precio": 200000,
                    "stock": 30,
                },
                {
                    "nombre": "Gabinete Cooler Master",
                    "descripcion_corta": "ATX RGB con panel de vidrio",
                    "descripcion": "Gabinete ATX con panel lateral de vidrio templado, 3 ventiladores RGB.",
                    "precio": 180000,
                    "stock": 35,
                },
            ],
            "Celulares": [
                {
                    "nombre": "iPhone 15 Pro",
                    "descripcion_corta": "Apple A17 Pro 256GB",
                    "descripcion": "iPhone 15 Pro con chip A17 Pro, 256GB, cámara triple 48MP, Dynamic Island.",
                    "precio": 2500000,
                    "descuento": 8,
                    "stock": 20,
                },
                {
                    "nombre": "Samsung Galaxy S24 Ultra",
                    "descripcion_corta": "Galaxy S24 Ultra 512GB",
                    "descripcion": "Teléfono Galaxy S24 Ultra con S Pen, cámara 200MP, pantalla Dynamic AMOLED 2X.",
                    "precio": 2700000,
                    "descuento": 5,
                    "stock": 15,
                },
                {
                    "nombre": "Xiaomi 13 Pro",
                    "descripcion_corta": "Xiaomi 13 Pro 256GB",
                    "descripcion": "Xiaomi 13 Pro con Snapdragon 8 Gen 2, pantalla AMOLED 120Hz, cámara Leica.",
                    "precio": 1800000,
                    "stock": 30,
                },
                {
                    "nombre": "OnePlus 12",
                    "descripcion_corta": "OnePlus 12 256GB",
                    "descripcion": "OnePlus 12 con Snapdragon 8 Gen 3, 16GB RAM, batería 5400mAh, carga 100W.",
                    "precio": 1600000,
                    "stock": 25,
                },
                {
                    "nombre": "Realme GT 6",
                    "descripcion_corta": "Realme GT 6 256GB",
                    "descripcion": "Realme GT 6 con Snapdragon 8s Gen 3, pantalla FHD+ 120Hz, carga 120W.",
                    "precio": 1400000,
                    "stock": 28,
                },
            ],
            "Audio": [
                {
                    "nombre": "Auriculares Bose QC45",
                    "descripcion_corta": "Bose QuietComfort 45 inalámbricos",
                    "descripcion": "Auriculares inalámbricos con cancelación de ruido activa, 24h de batería.",
                    "precio": 850000,
                    "descuento": 10,
                    "stock": 20,
                },
                {
                    "nombre": "Altavoz Sonos One SL",
                    "descripcion_corta": "Altavoz inteligente multiroom",
                    "descripcion": "Altavoz Sonos One SL con sonido envolvente, compatible con AirPlay 2.",
                    "precio": 450000,
                    "stock": 25,
                },
                {
                    "nombre": "Micrófono Boya BY-M1",
                    "descripcion_corta": "Micrófono lavalier omnidireccional",
                    "descripcion": "Micrófono de solapa omnidireccional con cable de 6m, compatible con smartphones.",
                    "precio": 25000,
                    "stock": 50,
                },
                {
                    "nombre": "Parlante Marshall Emberton",
                    "descripcion_corta": "Bocina portátil Bluetooth",
                    "descripcion": "Bocina portátil Marshall Emberton, sonido multidireccional, 20h batería.",
                    "precio": 280000,
                    "stock": 18,
                },
                {
                    "nombre": "Audífonos Sony MDR-XB55AP",
                    "descripcion_corta": "Audífonos con cable extra bass",
                    "descripcion": "Audífonos intrauriculares con control remoto y micrófono, sonido extra bass.",
                    "precio": 80000,
                    "stock": 50,
                },
            ],
            "Gaming": [
                {
                    "nombre": "PlayStation 5 Slim",
                    "descripcion_corta": "PS5 Slim con disco 1TB",
                    "descripcion": "Consola PlayStation 5 Slim con unidad de disco, 1TB SSD, mando DualSense.",
                    "precio": 2000000,
                    "descuento": 5,
                    "stock": 20,
                },
                {
                    "nombre": "Xbox Series X",
                    "descripcion_corta": "Xbox Series X 1TB SSD",
                    "descripcion": "Consola Xbox Series X con 1TB SSD, 120FPS, retrocompatible con Xbox One.",
                    "precio": 1900000,
                    "stock": 25,
                },
                {
                    "nombre": "Nintendo Switch OLED",
                    "descripcion_corta": "Nintendo Switch pantalla OLED",
                    "descripcion": "Nintendo Switch con pantalla OLED de 7 pulgadas, 64GB, dock con LAN.",
                    "precio": 900000,
                    "stock": 35,
                },
                {
                    "nombre": "Mando Xbox Wireless",
                    "descripcion_corta": "Mando inalámbrico Xbox carbon black",
                    "descripcion": "Mando inalámbrico Xbox con textura ergonómica, batería de larga duración.",
                    "precio": 120000,
                    "stock": 60,
                },
                {
                    "nombre": "Mouse Razer DeathAdder V2",
                    "descripcion_corta": "Mouse gaming 20000 DPI",
                    "descripcion": "Mouse ergonómico para gaming con sensor óptico de 20000 DPI, switches ópticos.",
                    "precio": 150000,
                    "descuento": 10,
                    "stock": 45,
                },
            ],
            "Oficina": [
                {
                    "nombre": "Escritorio Eléctrico Ajustable",
                    "descripcion_corta": "Mesa eléctrica altura adjustable",
                    "descripcion": "Escritorio eléctrico con altura ajustable, panel de control digital, 120x60cm.",
                    "precio": 450000,
                    "stock": 10,
                },
                {
                    "nombre": "Silla Ejecutiva Ergonómica",
                    "descripcion_corta": "Silla de oficina con soporte lumbar",
                    "descripcion": "Silla ejecutiva con respaldo alto, soporte lumbar ajustable, reposabrazos 3D.",
                    "precio": 650000,
                    "descuento": 10,
                    "stock": 15,
                },
                {
                    "nombre": "Impresora HP LaserJet Pro",
                    "descripcion_corta": "Impresora láser monocromática",
                    "descripcion": "Impresora láser HP LaserJet Pro, impresión dúplex automática, WiFi.",
                    "precio": 380000,
                    "stock": 20,
                },
                {
                    "nombre": "Escáner Epson Perfection V600",
                    "descripcion_corta": "Escáner de sobremesa A4",
                    "descripcion": "Escáner de sobremesa con resolución 6400x9600 dpi, para fotos y documentos.",
                    "precio": 280000,
                    "stock": 25,
                },
                {
                    "nombre": "Estantería Metálica 5 Niveles",
                    "descripcion_corta": "Estantería archivo metálica",
                    "descripcion": "Estantería de archivos metálica de 5 niveles, 90x35x180cm, color negro.",
                    "precio": 180000,
                    "stock": 30,
                },
            ],
        }

        produtos_creados = 0
        self.stdout.write("Creando productos...")
        for nombre_cat, productos_lista in data.items():
            categoria = Categoria.objects.get(nombre=nombre_cat)
            for prod in productos_lista:
                obj, creado = Producto.objects.get_or_create(
                    nombre=prod["nombre"],
                    defaults={
                        "descripcion_corta": prod.get("descripcion_corta", ""),
                        "descripcion": prod["descripcion"],
                        "precio": Decimal(str(prod["precio"])),
                        "descuento": Decimal(str(prod.get("descuento", 0))),
                        "stock": prod["stock"],
                        "categoria": categoria,
                        "activo": True,
                        "destacado": prod.get("descuento", 0) > 0,
                    },
                )
                if creado:
                    produtos_creados += 1
                    self.stdout.write(f"  ✓ {prod['nombre']}")
                else:
                    self.stdout.write(f"  - {prod['nombre']} (ya existe)")

        self.stdout.write(f"\n✓ {produtos_creados} productos creados")
        self.stdout.write(f"✓ {categorias_creadas} categorías creadas\n")
