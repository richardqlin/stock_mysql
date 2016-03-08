from django import forms
from .models import Stock,User,Location


class StockForm(forms.ModelForm):	
	class Meta:
		model=Stock
		fields='__all__'
			
		
class LocationForm(forms.ModelForm):
	prefix='username'
	class Meta:
		model=Location
		fields='__all__'
			