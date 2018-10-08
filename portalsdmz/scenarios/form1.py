from django import forms

class ScenarioForminit(forms.Form,ip):

		print"ip da form 1"
		print ip
		ip_remoto	= forms.CharField(max_length = 120, initial = '172.20.5.38', widget=forms.TextInput(attrs={'class': 'col-sm-5'}))
