#!/usr/bin/python

import subprocess, re, sys, time, csv, os
from measureTools.models import iperfData

def iniciarIperf3Remoto(hostname):
	print "\nIniciando iperf3 remoto ...\n"
	subprocess.Popen(['ssh', hostname, 'iperf3', '-s'])
	subprocess.call(['sleep', '2'])
	print"\n\n"

def finalizarIperf3Remoto(hostname):
	print"Finalizando qualquer iperf3 iniciado ..."
	subprocess.call(['ssh', hostname, 'killall', 'iperf3'])
	subprocess.call(['sleep', '2'])

def converteBandwidthParaMb(bandwidth):
	if bandwidth == 'G':
		return 1024
	elif bandwidth == 'M':
		return 1
	else:
		return 0

def runIperf(ip_remoto, fluxo, tamanho, numero_teste):
	print("Iniciando teste "+ str(numero_teste) +" do iperf3 para" + tamanho)
	cmd = 'iperf3 -c ' + ip_remoto + ' -P ' + str(fluxo) + ' -i1 -O 5 -n ' + tamanho
	return subprocess.check_output(cmd, shell=True)

def filterIperfResult(iperf_result, fluxo):
	regex_bw	 	= '([\d.]* [A-Z])\w+/sec'
	regex_letter 	= '[A-Za-z]'
	regex_digit 	= '[\d.]*'
	lista_bw = re.findall(regex_bw,iperf_result)
	bandwidth = lista_bw[-1]
	bandwidth_size	= re.findall(regex_letter, bandwidth)[0]
	bandwidth = re.findall(regex_digit,bandwidth)[0]
	bandwidth = "{0:0.1f}".format(float(bandwidth)*converteBandwidthParaMb(bandwidth_size))
	return bandwidth

def saveIperfResult(velocidade, cenario, descricao_erro, numero_teste):
 	s = iperfData(velocidade = velocidade, scenario = cenario, descricao_erro = descricao_erro, num_teste = numero_teste)
	s.save()

def iperfTool(ip_remoto, tamanho, numero_teste, fluxo, cenario):
	user 			= 'sdmz'
	data     		= time.strftime('%d/%m %H:%M:%S')
	hostname 		= user + '@' + ip_remoto
	descricao_erro  = ''

	print"\n\n\n>>>>> Iniciando iperf3 para teste de MEMORIA a MEMORIA"

	try:
		finalizarIperf3Remoto(hostname)
		iniciarIperf3Remoto(hostname)
		iperf_result = runIperf(ip_remoto, fluxo, tamanho, numero_teste)
		bandwidth = filterIperfResult(iperf_result, fluxo)
		saveIperfResult(bandwidth, cenario, descricao_erro, numero_teste)
	except Exception as e:
		saveIperfResult(0, cenario, e, numero_teste)

	print "\n>>> Finalizando o script <<<"
