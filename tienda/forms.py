from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, Pedido, ItemCarrito


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "descripcion_corta",
            "descripcion",
            "precio",
            "descuento",
            "stock",
            "categoria",
            "imagen",
            "activo",
            "destacado",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del producto"}
            ),
            "descripcion_corta": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Breve descripción (máx 200 caracteres)",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Descripción", "rows": 4}
            ),
            "precio": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "0.00"}
            ),
            "descuento": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "0"}
            ),
            "stock": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "0"}
            ),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "imagen": forms.FileInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "destacado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio is None:
            raise forms.ValidationError("El precio es obligatorio.")
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que 0.")
        return precio

    def clean_descuento(self):
        descuento = self.cleaned_data.get("descuento", 0)
        if descuento < 0 or descuento > 100:
            raise forms.ValidationError("El descuento debe estar entre 0 y 100.")
        return descuento


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}
        ),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Tu nombre"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Tu apellido"}
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Nombre de usuario"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Contraseña"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirmar contraseña"}
        )


class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Apellido"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            "nombre",
            "direccion",
            "ciudad",
            "telefono",
            "email",
            "notas",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre completo"}
            ),
            "direccion": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Calle, número, depto"}
            ),
            "ciudad": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ciudad"}
            ),
            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+56 9 1234 5678",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "correo@ejemplo.com",
                }
            ),
            "notas": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Instrucciones especiales (opcional)",
                }
            ),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")
        if not telefono:
            raise forms.ValidationError("El teléfono es obligatorio.")
        return telefono


class CarritoForm(forms.ModelForm):
    class Meta:
        model = ItemCarrito
        fields = ["cantidad"]
        widgets = {
            "cantidad": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "min": 1,
                    "style": "width: 70px;",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        self.producto = kwargs.pop("producto", None)
        super().__init__(*args, **kwargs)

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get("cantidad")
        if cantidad < 1:
            raise forms.ValidationError("La cantidad mínima es 1.")
        if self.producto and cantidad > self.producto.stock:
            raise forms.ValidationError(
                f"Solo hay {self.producto.stock} unidades disponibles."
            )
        return cantidad
