from django import forms
from .models import Producto, Categoria


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "stock", "categoria", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del producto"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripción", "rows": 3}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0.00"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio.")
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio is None:
            raise forms.ValidationError("El precio es obligatorio.")
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que 0.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock

    def clean_categoria(self):
        categoria = self.cleaned_data.get("categoria")
        if not categoria:
            raise forms.ValidationError("La categoría es obligatoria.")
        return categoria
