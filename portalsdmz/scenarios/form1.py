from django import forms

class ScenarioForminit(forms.Form):

		ip_remoto	= forms.CharField(max_length = 120, initial = 'dtn.sciencedmz.usp.br', widget=forms.TextInput(attrs={'class': 'col-sm-5'}))
