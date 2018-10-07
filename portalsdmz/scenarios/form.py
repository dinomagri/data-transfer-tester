from django import forms
import datetime
from whichcraft import which
import subprocess

#from .views import

SIZE_CHOICES = (
	("1G",   '1G              '),
	("10G",  '10G             '),
	("100G", '100G            ')
)


class ScenarioForm(forms.Form):


		nome 		= forms.CharField(max_length = 120, initial='Teste', widget=forms.TextInput(attrs={'class': 'col-sm-5'}))
		data 		= forms.DateTimeField(initial = datetime.datetime.now(), widget=forms.HiddenInput())
		tamanho 	= forms.ChoiceField(choices=SIZE_CHOICES, widget=forms.Select(attrs={'class': 'col-sm-5'}))
#		ip_remoto	= forms.CharField(max_length = 120, initial = '172.20.5.38', widget=forms.TextInput(attrs={'class': 'col-sm-5'}))
		limite		= forms.IntegerField(initial = 1, min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class': 'col-sm-5'}))
		destino		= forms.CharField(max_length = 120, initial = 'dados/area-teste', widget=forms.TextInput(attrs={'class': 'col-sm-5'}))
		origem		= forms.CharField(max_length = 120, initial = 'dados/area-teste', widget=forms.TextInput(attrs={'class': 'col-sm-5'}))
		fluxo		= forms.IntegerField(initial = 1, min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class': 'col-sm-5'}))

		scp 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		wget		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		udr 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		iperf 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		gridftp		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		axel 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		aria2c 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		xrootd 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		fdt 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))

class ScenarioForminit(forms.Form):

		ip_remoto	= forms.CharField(max_length = 120, initial = '172.20.5.38', widget=forms.TextInput(attrs={'class': 'col-sm-5'}))
