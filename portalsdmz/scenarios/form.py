from django import forms
import datetime
from whichcraft import which
import subprocess


SIZE_CHOICES = (
	("1G",   '1G              '),
	("10G",  '10G             '),
	("100G", '100G            ')
)


class ScenarioForm(forms.Form):


		nome 		= forms.CharField(max_length = 120, initial='Teste', widget=forms.TextInput(attrs={'class': 'col-sm-5'}))
		data 		= forms.DateTimeField(initial = datetime.datetime.now(), widget=forms.HiddenInput())
		tamanho 	= forms.ChoiceField(choices=SIZE_CHOICES, widget=forms.Select(attrs={'class': 'col-sm-5'}))
		ip_remoto	= forms.CharField(max_length = 120, initial = 'dtn.sciencedmz.usp.br', widget=forms.HiddenInput())
		limite		= forms.IntegerField(initial = 1, min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class': 'col-sm-5'}))
		destino		= forms.CharField(max_length = 120, initial = 'dados/area-teste', widget=forms.TextInput(attrs={'class': 'col-sm-5'}))
		origem		= forms.CharField(max_length = 120, initial = 'dados/area-teste', widget=forms.TextInput(attrs={'class': 'col-sm-5'}))
		fluxo		= forms.IntegerField(initial = 1, min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class': 'col-sm-5'}))

		print 'antes do form do scp'

# 		def __init__(self, *args, **kwargs):
# 					super(ScenarioForm, self).__init__(*args, **kwargs)
#                 # now we add each question individually
# 					path_tools = {}
# 					tools = ['aria2c', 'wget', 'axel', 'globus-url-copy',  'iperf', 'scp', 'udt', 'xrootd','fdt.jar']
# 					for tool in tools:
# 						path_tools[tool] = which(tool)
# 					print path_tools
# 					print IP
#
# #					for key, value in path_tools.items():
# #						if value != None:
# #							if key == 'globus-url-copy':
# #								self.fields['gridftp'] = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
# #							self.fields[key] = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
#
#
# #					Ip = getIP()
# #					Ip = request.session['ip_remoto']
# 					print("Iniciando obtencao de ferramenta remota")
# 					cmd = 'ssh sdmz@dtn.sciencedmz.usp.br python /tmp/script.py'
#
# 				 	path_tools2 = subprocess.check_output(cmd, shell=True)
# #					path_tools2
# #					path_tools2 = list()
# 					print path_tools2
# #					print path_tools2.split()
# #					try:
# 					tools = eval(path_tools2)
# #					except:
#
#
#
#
# 					for key, value in path_tools.items():
# 						for key2, value2 in tools.items():
# 							if value != None:
# 								if value2 != None and key2 == key :
# 									if key == 'globus-url-copy':
# 										self.fields['gridftp'] = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
# 									else:
# 										self.fields[key] = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
#

		scp 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		wget		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
#		udr 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		iperf 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		gridftp		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		axel 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		aria2c 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		xrootd 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))
		fdt 		= forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': ''}))

class ScenarioForminit(forms.Form):

		ip_remoto	= forms.CharField(max_length = 120, initial = 'dtn.sciencedmz.usp.br', widget=forms.TextInput(attrs={'class': 'col-sm-5'}))
