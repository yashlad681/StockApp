from django import forms 
from .models import Stock

class Stockform(forms.ModelForm):
    class Meta:
        model = Stock
        fields= ["ticker"]