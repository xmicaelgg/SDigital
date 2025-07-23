from django import forms

class IMEIForm(forms.Form):
    MODELO_CHOICES = [
        ('generico', 'Genérico'),
        ('mojo', 'Mojo'),
    ]
    modelo = forms.ChoiceField(choices=MODELO_CHOICES, label='Modelo', initial='generico')
    raw_text = forms.CharField(
        label='Pega aquí los IMEIs',
        widget=forms.Textarea(attrs={'rows': 10, 'placeholder': 'Pega los IMEIs aquí, uno por línea o separados por espacios.'})
    ) 