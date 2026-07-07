import os
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings

from tienda.models import Producto

# Mapa manual: nombre exacto del producto -> nombre del archivo (sin extensión)
MANUAL_MAP = {
    "Notebook Lenovo IdeaPad 5": "notebook-lenovo-ideapad-5",
    "Monitor Samsung 27\"": "monitor-samsung-27",
    "Teclado Mecánico Redragon": "teclado-mecanico-redragon",
    "Parlante JBL Flip": "parlante-jbl-flip",
    "Impresora HP Smart Tank": "impresora-hp-smart-tank",
    "Tarjeta gráfica NVIDIA RTX 3060": "tarjeta-grafica-nvidia-rtx-3060",
    "Samsung Galaxy S24 Ultra": "telefono",
    "Xiaomi Mi 13": "xiaomi-mi-13",
    "Altavoz Sonos One": "altavoz-sonos-one",
    "Xbox Series X": "xbox-series-x",
    "Impresora láser HP LaserJet Pro": "impresora-laser-hp-laserjet-pro",
    "Escáner Epson 2200": "escaner-epson-2200",
    "Mouse Logitech G203": "mouse-logitech-g203",
    "SSD Kingston 1TB": "ssd-kingston-1tb",
    "Memoria RAM Corsair 16GB": "memoria-ram-corsair-16gb",
    "Audífonos Sony WH-CH520": "audifonos-sony-wh-ch520",
    "Webcam Logitech C920": "webcam-logitech-c920",
    "Procesador Intel i7 12ª Gen": "procesador-intel-i7-12-generacion",
    "Tarjeta Gráfica RTX 3060": "tarjeta-grafica-nvidia-rtx-3060",
    "Disco Duro WD 4TB": "disco-duro-western-digital-4tb",
    "Fuente Poder Corsair 750W": "fuente-de-poder-corsair-750w",
    "Gabinete Cooler Master": "caja-pc-cooler-master",
    "iPhone 15 Pro": "iphone-15-pro",
    "Xiaomi 13 Pro": "xiaomi-mi-13",
    "OnePlus 12": "oneplus-12",
    "Realme GT 6": "realme-gt-6",
    "Auriculares Bose QC45": "auriculares-bose-quietcomfort-45",
    "Altavoz Sonos One SL": "altavoz-sonos-one",
    "Micrófono Boya BY-M1": "microphone-boya-y515",
    "Parlante Marshall Emberton": "parlante-jbl-flip",
    "Audífonos Sony MDR-XB55AP": "auriculares-con-cable-sony-mdr-xb55ap",
    "PlayStation 5 Slim": "playstation-5",
    "Nintendo Switch OLED": "nintendo-switch-oled",
    "Mando Xbox Wireless": "joystick-xbox-series-x",
    "Mouse Razer DeathAdder V2": "raton-para-juegos-razer-kiyo",
    "Escritorio Eléctrico Ajustable": "escritorio-de-oficina-ikea",
    "Silla Ejecutiva Ergonómica": "silla-ejecutiva-mr-dork",
    "Impresora HP LaserJet Pro": "impresora-laser-hp-laserjet-pro",
    "Escáner Epson Perfection V600": "escaner-epson-2200",
    "Estantería Metálica 5 Niveles": "estanteria-de-archivos-metalica",
}


class Command(BaseCommand):
    help = "Sube imágenes locales a Cloudinary y las asigna a cada producto"

    def handle(self, *args, **options):
        if not all(os.environ.get(k) for k in ("CLOUDINARY_CLOUD_NAME", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET")):
            self.stdout.write(self.style.WARNING(
                "Cloudinary no está configurado (faltan CLOUDINARY_CLOUD_NAME, "
                "CLOUDINARY_API_KEY y/o CLOUDINARY_API_SECRET).\n"
                "Este comando solo es necesario en producción (Render). "
                "Localmente las imágenes se sirven desde el fallback Cloudinary 'wf4xjrci'."
            ))
            return

        media_dir = settings.MEDIA_ROOT
        productos_dir = os.path.join(media_dir, "productos")

        if not os.path.isdir(productos_dir):
            self.stdout.write(self.style.ERROR(
                f"No se encontró el directorio: {productos_dir}"
            ))
            return

        # Indexar archivos disponibles por slug (sin extensión)
        known_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
        file_index = defaultdict(list)

        for f in os.listdir(productos_dir):
            full = os.path.join(productos_dir, f)
            if not os.path.isfile(full):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext not in known_extensions:
                continue
            slug = os.path.splitext(f)[0].lower()
            file_index[slug].append(full)

        def pick_best(paths):
            priority = {".webp": 0, ".jpg": 1, ".jpeg": 1, ".png": 2, ".gif": 3, ".bmp": 4}
            paths.sort(key=lambda p: priority.get(os.path.splitext(p)[1].lower(), 99))
            return paths[0]

        ok_count = 0
        no_match = []

        for producto in Producto.objects.all().order_by("id"):
            target_slug = MANUAL_MAP.get(producto.nombre)
            if not target_slug:
                no_match.append(f"{producto.nombre} (sin entrada en MANUAL_MAP)")
                continue

            candidates = file_index.get(target_slug, [])
            if not candidates:
                no_match.append(f"{producto.nombre} (archivo '{target_slug}' no encontrado)")
                continue

            path = pick_best(candidates)
            with open(path, "rb") as fh:
                filename = os.path.basename(path)
                producto.imagen = File(fh, name=filename)
                producto.save()
            ok_count += 1
            self.stdout.write(f"  ✓ {producto.nombre} -> {filename}")

        self.stdout.write(f"\nProductos actualizados: {ok_count}/{Producto.objects.count()}")

        if no_match:
            self.stdout.write(self.style.WARNING(f"\nProductos sin imagen ({len(no_match)}):"))
            for n in no_match:
                self.stdout.write(f"  - {n}")

        # Mostrar archivos no usados
        used = set()
        for producto in Producto.objects.all():
            if producto.imagen:
                used.add(os.path.basename(producto.imagen.name))
        all_files = set()
        for paths in file_index.values():
            for p in paths:
                all_files.add(os.path.basename(p))
        unused = all_files - used
        if unused:
            self.stdout.write(self.style.WARNING(f"\nArchivos no asignados ({len(unused)}):"))
            for f in sorted(unused):
                self.stdout.write(f"  - {f}")

        self.stdout.write(self.style.SUCCESS("\nMigración completada."))
