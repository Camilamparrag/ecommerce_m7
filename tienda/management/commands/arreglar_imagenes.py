import os
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from tienda.models import Producto

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
    help = "Asigna imágenes locales a cada producto (FileSystemStorage local / Cloudinary en producción)"

    def handle(self, *args, **options):
        productos_dir = os.path.join(settings.MEDIA_ROOT, "productos")

        if not os.path.isdir(productos_dir):
            self.stdout.write(self.style.ERROR(
                f"No se encontró el directorio: {productos_dir}"
            ))
            return

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

        ok = 0
        errors = []
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
            basename = os.path.basename(path)
            storage = Producto.imagen.field.storage

            try:
                if isinstance(storage, FileSystemStorage):
                    producto.imagen.name = f"productos/{basename}"
                    producto.save(update_fields=["imagen"])
                else:
                    with open(path, "rb") as fh:
                        producto.imagen = File(fh, name=basename)
                        producto.save()
                ok += 1
                self.stdout.write(f"  ✓ {producto.nombre} -> {basename}")
            except Exception as e:
                errors.append(f"{producto.nombre}: {e}")
                self.stdout.write(self.style.ERROR(f"  ✗ {producto.nombre}: {e}"))

        total = Producto.objects.count()
        self.stdout.write(f"\nActualizados: {ok}/{total}")

        if errors:
            self.stdout.write(self.style.ERROR(f"\nErrores ({len(errors)}):"))
            for e in errors:
                self.stdout.write(f"  - {e}")

        if no_match:
            self.stdout.write(self.style.WARNING(f"\nSin imagen ({len(no_match)}):"))
            for n in no_match:
                self.stdout.write(f"  - {n}")

        self.stdout.write(self.style.SUCCESS("Listo."))
