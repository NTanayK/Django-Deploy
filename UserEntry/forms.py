from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['name', 'email', 'department', 'phone_number', 'slap', 'campus']  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'department': forms.TextInput(attrs={'class': 'input-field'}),
            'phone_number': forms.TextInput(attrs={'class': 'input-field'}),
            'slap': forms.TextInput(attrs={'class': 'input-field'}),
            'campus': forms.TextInput(attrs={'class': 'input-field'}), 
        }
