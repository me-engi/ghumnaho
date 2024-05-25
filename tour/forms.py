# tours/forms.py
from django import forms
from .models import Tour, Image  # Import models locally within the form

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['name', 'description', 'price', 'max_participants', 'images']
        widgets = {
            'images': forms.ClearableFileInput(attrs={'multiple': True}),
        }
