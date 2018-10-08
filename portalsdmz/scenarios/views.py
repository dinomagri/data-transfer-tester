from django.views import generic
from whichcraft import which

import subprocess

import datetime
from django.shortcuts import (
	render_to_response, RequestContext
)
from django.utils import timezone

from chartit import DataPool, Chart

from .form import ScenarioForm,ScenarioForminit
from .form1 import ScenarioForminit
from .models import	(
	ScenarioData, ScenarioTimeData
)
from measureTools.lib import (
	gridftpTool, iperfTool, scpTool, wgetTool, axelTool, udrTool, aria2cTool, xrootdTool, fdtTool
)
from measureTools.models import (
	gridftpData, iperfData, scpData, wgetData, axelData, udrData, aria2cData, xrootdData, fdtData
)

from django.http import HttpResponse
from django import forms

IP = "dtn.sciencedmz.usp.br"

iperf=wget=gridftp=axel=udr=aria2c=xrootd=fdt=scp=False


def runScripts(nome, data, tamanho, ip_remoto, limite, destino, origem, fluxo, iperf, scp, wget, gridftp, axel, udr, aria2c, xrootd, fdt):

	scenario = ScenarioData(nome = nome, data_inicio = data, tamanho = tamanho)
	scenario.save()
	print "-------------"
	print nome
	print data
	print tamanho
	for i in range(1, limite+1):

		startTime = datetime.datetime.now()
		#startTime = nowStart.strftime('%d-%m-%Y %H:%M')
		print startTime
		if iperf :
			print 'executando iperf'
			iperfTool.iperfTool(ip_remoto, tamanho, i, fluxo, scenario)
		if scp :
			print 'executando scp'
			scpTool.scpTool(ip_remoto, tamanho, i, origem, destino, scenario)
		if wget :
			print 'executando wget'
			wgetTool.wgetTool(ip_remoto, tamanho, i, destino, scenario)
		if gridftp :
			print 'executando gridftp'
			gridftpTool.gridftpTool(ip_remoto, tamanho, i, origem, destino, fluxo, scenario)
		if axel :
			print 'executando axel'
			axelTool.axelTool(ip_remoto, tamanho, i, origem, destino, fluxo, scenario)
		if udr :
			print 'executando udr'
			udrTool.udrTool(ip_remoto, tamanho, i, origem, destino, fluxo, scenario)
		if aria2c :
			print 'executando aria2c'
			aria2cTool.aria2cTool(ip_remoto, tamanho, i, origem, destino, fluxo, scenario)
		if xrootd :
			print 'executando xrootd'
			xrootdTool.xrootdTool(ip_remoto, tamanho, i, origem, destino, fluxo, scenario)
		if fdt :
			print 'executando fdt'
			fdtTool.fdtTool(ip_remoto, tamanho, i, origem, destino, fluxo, scenario)

		endTime = datetime.datetime.now()
		#endTime = nowEnd.strftime('%d-%m-%Y %H:%M')
		scenarioTime = ScenarioTimeData(data_inicio = startTime, data_fim = endTime, num_teste = i, cenario = scenario)
		scenarioTime.save()

	scenario.data_fim = datetime.datetime.now()
	#scenario.data_fim = nowDataFim.strftime('%d-%m-%Y %H:%M')

	scenario.save()

class scenarioHelper(generic.TemplateView):
	template_name = 'helper.html'

class newScenario(generic.FormView):


#		path_tools = {}
#		tools = ['aria2c', 'wget', 'axel', 'globus-url-copy', 'iperf', 'scp', 'udt']
#		for tool in tools:
#				path_tools[tool] = which(tool)
#		print path_tools


		template_name = 'scenarios/scenario/newscenario.html'
		form_class = ScenarioForm
		success_url = 'results'

		print "antes do inicio"



		def get(self, request, *args, **kwargs):
			print"entrou por causa do get 2"
			print IP
			form_class = self.get_form_class()
			form = self.get_form(form_class)
			context = self.get_context_data(**kwargs)
			context['form'] = form
			print("Iniciando obtencao de ferramenta remota")
			cmd = 'ssh sdmz@'+ IP +' python /tmp/script.py '

			path_tools2 = subprocess.check_output(cmd, shell=True)
			print path_tools2
			tools1 = eval(path_tools2)


			path_tools = {}
			tools = ['aria2c', 'wget', 'axel', 'globus-url-copy', 'iperf', 'scp', 'udt','xrootd','fdt.jar']
			for tool in tools:
					path_tools[tool] = which(tool)

			print "passou do basico"
			print path_tools
			for key,value in path_tools.iteritems():
				print "entou no for"
				for key2, value2 in tools1.items():
					if value == None:
						if value2 == None and key2 == key :
								if key == 'aria2c':
									aria2c		= form.fields['aria2c'].widget = forms.HiddenInput()
								if key == 'wget':
									wget		= form.fields['wget'].widget = forms.HiddenInput()
								if key == 'axel':
									axel		= form.fields['axel'].widget = forms.HiddenInput()
								if key == 'globus-url-copy':
									gridftp		= form.fields['gridftp'].widget = forms.HiddenInput()
								if key == 'xrootd':
									xrootd      = form.fields['xrootd'].widget = forms.HiddenInput()
								if key == 'iperf':
									iperf 		= form.fields['iperf'].widget = forms.HiddenInput()
								if key == 'scp':
									scp 		= form.fields['scp'].widget = forms.HiddenInput()
								if key == 'fdt':
									fdt     	= form.fields['fdt'].widget = forms.HiddenInput()

			return self.render_to_response(context)


		def form_valid(self, form):
			print "entrou depois"

#			print path_tools
			"""option_scp  	= form.cleaned_data.get("scp")
			option_wget  	= form.cleaned_data.get("wget")
			option_udr      = form.cleaned_data.get("udr")
			option_iperf	= form.cleaned_data.get("iperf")
			option_axel	= form.cleaned_data.get("axel")
			option_gridftp	= form.cleaned_data.get("gridftp")
			option_aria2c	= form.cleaned_data.get("aria2c")
			fluxo_valid 	= form.cleaned_data.get("fluxo")"""

			# iperf=wget=gridftp=axel=udr=aria2c=xrootd=fdt=scp= False
#			scp = True

			nome 		= form.cleaned_data['nome']
			data 		= form.cleaned_data['data']
			tamanho 	= form.cleaned_data['tamanho']
			limite		= form.cleaned_data['limite']
			ip_remoto	= form.cleaned_data['ip_remoto']
			destino		= form.cleaned_data['destino']
			origem		= form.cleaned_data['origem']
			fluxo		= form.cleaned_data['fluxo']



#			Ip = getIP()
#			print Ip
			# print("Iniciando obtencao de ferramenta remota")
			# cmd = 'ssh sdmz@dtn.sciencedmz.usp.br python /tmp/script.py '
			#
			# path_tools2 = subprocess.check_output(cmd, shell=True)
			# print path_tools2
			# tools1 = eval(path_tools2)
			#
			#
			# path_tools = {}
			# tools = ['aria2c', 'wget', 'axel', 'globus-url-copy', 'iperf', 'scp', 'udt','xrootd','fdt.jar']
			# for tool in tools:
			# 		path_tools[tool] = which(tool)
			#
			# print "passou do basico"
			# print path_tools
			# for key,value in path_tools.iteritems():
			# 	print "entou no for"
			# 	for key2, value2 in tools1.items():
			# 		if value != None:
			# 			if value2 != None and key2 == key :
			# 					if key == 'aria2c':
			# 						aria2c		= form.cleaned_data['aria2c']
			# 					if key == 'wget':
			# 						wget		= form.cleaned_data['wget']
			# 					if key == 'axel':
			# 						axel		= form.cleaned_data['axel']
			# 					if key == 'globus-url-copy':
			# 						gridftp		= form.cleaned_data['gridftp']
			# 					if key == 'xrootd':
			# 						xrootd      = form.cleaned_data['xrootd']
			# 					if key == 'iperf':
			# 						iperf 		= form.cleaned_data['iperf']
			# 					if key == 'scp':
			# 						scp 		= form.cleaned_data['scp']
			# 					if key == 'udt':
			# 						udr		= form.cleaned_data['udt']
			# 					if key == 'fdt':
			# 						fdt      = form.cleaned_data['fdt']
#					print  scp

			"""if option_scp == 'False' or option_iperf == 'False' or option_wget == 'False' or option_gridftp == 'False' or option_axel == 'False' or option_udr == 'False' or option_aria2c == 'False':

				raise forms.ValidationError("Error. All fields empty")"""
			print "an tes do return"
			runScripts(nome, data, tamanho, ip_remoto, limite, destino, origem, fluxo, iperf, scp, wget, gridftp, axel, udr, aria2c, xrootd, fdt)
			return super(newScenario, self).form_valid(form)

class newScenarioInit(generic.FormView):

		template_name = 'scenarios/newscenarioinit.html'
		form_class = ScenarioForminit
		success_url = 'scenarios/scenario'

		def get(self, request, *args, **kwargs):
			print"entrou por causa do get"
			form_class = self.get_form_class()
			form = self.get_form(form_class)
			context = self.get_context_data(**kwargs)
			context['form'] = form
			return self.render_to_response(context)

		def form_valid(self, form):
			print "entrou depois"

			ip_remoto	= form.cleaned_data['ip_remoto']

			IP = ip_remoto
			print 'setou o ip'

			return super(newScenarioInit, self).form_valid(form)

class scenarioList(generic.ListView):
	template_name = 'scenarios/scenario_list.html'
	context_object_name = 'scenario_list'

	def get_queryset(self):
		return ScenarioData.objects.all

class scenarioResults(generic.ListView):
	template_name = 'scenarios/scenario_results.html'
	context_object_name = 'scenario_results'

	def mount_query_results(self):

		udrResults = udrData.objects.all().filter(scenario = self.scenario_id)
		if udrResults:
			self.queryResult['udr'] = udrResults

		axelResults = axelData.objects.all().filter(scenario = self.scenario_id)
		if axelResults:
			self.queryResult['axel'] = axelResults

		iperfResults = iperfData.objects.all().filter(scenario=self.scenario_id)
		if iperfResults:
			self.queryResult['iperf'] = iperfResults

		aria2cResults = aria2cData.objects.all().filter(scenario = self.scenario_id)
		if aria2cResults:
			self.queryResult['aria2c'] = aria2cResults

		wgetResults = wgetData.objects.all().filter(scenario=self.scenario_id)
		if wgetResults:
			self.queryResult['wget'] = wgetResults

		scpResults = scpData.objects.all().filter(scenario=self.scenario_id)
		if scpResults:
			self.queryResult['scp'] = scpResults

		gridftpResults = gridftpData.objects.all().filter(scenario=self.scenario_id)
		if gridftpResults:
			self.queryResult['gridftp'] = gridftpResults

		xrootdResults = xrootdData.objects.all().filter(scenario=self.scenario_id)
		if xrootdResults:
			self.queryResult['xrootd'] = xrootdResults

		fdtResults = fdtData.objects.all().filter(scenario=self.scenario_id)
		if fdtResults:
			self.queryResult['fdt'] = fdtResults

	def count_results(self):
		num_results = max([
			wgetData.objects.all().filter(scenario=self.scenario_id).count(),
			scpData.objects.all().filter(scenario=self.scenario_id).count(),
			iperfData.objects.all().filter(scenario=self.scenario_id).count(),
			gridftpData.objects.all().filter(scenario=self.scenario_id).count(),
			axelData.objects.all().filter(scenario = self.scenario_id).count(),
			udrData.objects.all().filter(scenario = self.scenario_id).count(),
			aria2cData.objects.all().filter(scenario = self.scenario_id).count(),
			xrootdData.objects.all().filter(scenario = self.scenario_id).count(),
			fdtData.objects.all().filter(scenario = self.scenario_id).count()
		])

		return num_results

	def serialize_query_results(self):
		scenario = ScenarioData.objects.get(pk=self.scenario_id)
		self.serializedQuery['scenario']= scenario

		num_results = self.count_results()

		self.serializedQuery['keys'] = {}
		for key in self.queryResult:
			self.serializedQuery['keys'][key] = 'foo'

		chart = self.generate_scenario_graph()
		self.serializedQuery['chart'] = chart

		self.serializedQuery['data'] = []
		for i in range(1, num_results+1):
			data = {}
			data['num_teste'] = i
			data['inicio'] = ScenarioTimeData.objects.get(cenario = self.scenario_id, num_teste = i).data_inicio
			data['fim'] = ScenarioTimeData.objects.get(cenario = self.scenario_id, num_teste = i).data_fim
			data['velocidade'] = {}
			for key in self.queryResult:
				data['velocidade'][key] = float(self.queryResult[key][i-1].velocidade)
			self.serializedQuery['data'].append(data)

	def generate_scenario_graph(self):
		series = []
		for key in self.queryResult:
			series.append({
				'options': {'source': self.queryResult[key]},
				'terms': [
					{('num_teste_'+key): 'num_teste'},
					{('velocidade_'+key): 'velocidade'}]
			})
		scenarioData = DataPool(series=series)

		series_options = [{
						'options': {
							'type': 'line',
							'stacking': False
						},
						'yAxis': 0,
						'xAxis': 0
						}]
		series_options[0]['terms'] = {}
		for key in self.queryResult:
			series_options[0]['terms']['num_teste_'+key] = ['velocidade_'+key]
		cht = Chart(
				datasource = scenarioData,
				series_options = series_options,
				chart_options = {
					'title': {'text': 'Velocidade em Mbit/s'},
					'yAxis':{'min': 0},
					'xAxis':{'title': {'text': 'Transferencia'}}
				}
			)
		return cht

	def get_queryset(self):
		self.queryResult = {}
		self.serializedQuery = {}
		self.scenario_id = self.kwargs['pk']

		self.mount_query_results()
		print self.queryResult

		self.serialize_query_results()
		print self.serializedQuery

		return self.serializedQuery


"""
queryResult = {
	'wget': [
		<wgetData:1>,
		<wgetData:2>,
		...
	]
	'iperf': [
		<iperfData:1>,
		<iperfData:2>,
		...
	]
	'scp': [
		<scpData:1>,
		<scpData:2>,
		...
	]
	'gridftp': [
		<gridftpData:1>,
		<gridftpData:2>,
		...
	]
}


serializedQuery = {
	'scenario': {
		'nome': 	nome
		'tamanho': 	tamanho
		'data': 	data
	}
	'keys':{
		'num_teste':'foo',
		'inicio': 	'foo',
		'fim':		'foo',
		'wget':		'foo',
		'iperf': 	'foo',
		'scp': 		'foo',
		'gridftp: 	'foo'
	}
	'data':
	[
		{
		'num_teste':i
		'inicio':	tempo_inicio
		'fim':		tempo_fim
		'velocidade':{
			'wget':		velocidadeWget
			'iperf':	velocidadeIperf
			'scp':		velocidadeScp
			'gridftp':	velocidadeGridftp
			}
		},
		{
		'wget':		velocidadeWget
		'iperf':	velocidadeIperf
		'scp':		velocidadeScp
		'gridftp':	velocidadeGridftp
		},
		...
	]
	'chart': chart
}
"""
