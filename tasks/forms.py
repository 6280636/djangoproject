from django.forms import ModelForm
from .models import Task
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']

class EmployeeLoginForm(forms.Form):
    """
    Formulaire de connexion utilisant uniquement le numéro d'employé.
    """
    employee_number = forms.IntegerField(
        label="Numéro d'employé",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre numéro d\'employé'
        })
    )