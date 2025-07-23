from django import forms
from .models import Lote, LoteDetalle, EstadoEnum, ModeloEquipo, LoteModelo

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['numero_lote', 'descripcion', 'cantidad_modelos']
        widgets = {
            'numero_lote': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de lote'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del lote'
            }),
            'cantidad_modelos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Cantidad de modelos'
            })
        }

class ModeloEquipoForm(forms.ModelForm):
    class Meta:
        model = ModeloEquipo
        fields = ['marca', 'modelo']
        widgets = {
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marca'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modelo'
            })
        }

class LoteDetalleForm(forms.ModelForm):
    class Meta:
        model = LoteDetalle
        fields = ['marca', 'modelo', 'imei', 'estado', 'caja_original', 'observaciones']
        widgets = {
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marca del equipo'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modelo del equipo'
            }),
            'imei': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IMEI (15 dígitos)',
                'pattern': r'\d{15}',
                'title': 'El IMEI debe tener exactamente 15 dígitos numéricos'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'caja_original': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            })
        }

class LoteModeloForm(forms.ModelForm):
    class Meta:
        model = LoteModelo
        fields = ['lote', 'marca', 'modelo']
        widgets = {
            'lote': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
        }

class ImportarExcelForm(forms.Form):
    lote = forms.ModelChoiceField(
        queryset=Lote.objects.all(),
        empty_label="Seleccione un lote",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Lote"
    )
    archivo = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls,.csv'
        }),
        label="Archivo Excel/CSV",
        help_text="Formatos soportados: .xlsx, .xls, .csv"
    )

class IngresarImeisForm(forms.Form):
    modelo_equipo = forms.ModelChoiceField(
        queryset=ModeloEquipo.objects.all(),
        empty_label="Seleccione un modelo",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Modelo de Equipo"
    )
    imeis = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Ingrese los IMEIs, uno por línea'
        }),
        label="IMEIs",
        help_text="Ingrese un IMEI por línea"
    )

class LoteDetalleMarcaModeloForm(forms.ModelForm):
    class Meta:
        model = LoteDetalle
        fields = ['marca', 'modelo']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca del equipo'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo del equipo'}),
        }

class LoteModeloCantidadImeisForm(forms.Form):
    modelo = forms.ModelChoiceField(
        queryset=LoteModelo.objects.all(),
        label="Modelo (Marca/Modelo)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cantidad = forms.IntegerField(
        min_value=1,
        required=False,
        label="Cantidad de equipos",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'})
    )
    imeis = forms.CharField(
        required=False,
        label="IMEIs",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Pega los IMEIs aquí, uno por línea'})
    ) 