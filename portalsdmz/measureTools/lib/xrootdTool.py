#!/usr/bin/python

import time, subprocess, re
from measureTools.models import xrootdData

def iniciarXrootDRemoto(hostname, pasta_des):
	print "\nIniciando xrootd server remoto ...\n"
	subprocess.Popen(['ssh', hostname, 'xrootd ' + pasta_des + "-d"])
	subprocess.call(['sleep', '2'])
	print"\n\n"

def finalizarXrootDTRemoto(hostname):
	print"Finalizando qualquer xrootd iniciado ..."
	subprocess.call(['ssh', hostname, 'pkill xrootd'])
	subprocess.call(['sleep', '2'])

def removeLocalFile(pasta_des,tamanho):
	print "\nRemovendo arquivos e pasta local criadas para o recebimento ...\n"
	cmd = "rm /"+ pasta_des +"/" + tamanho + "_file"
	subprocess.check_call(cmd, shell=True)

def createRemoteFolder(pasta_des, pasta, usuario, ip_remoto):
	print "\nCriando pasta remota para envio de arquivos ...\n"
	cmd = "if [ ! -d " + "/" + pasta_des + "/" + pasta + " ] ; then mkdir -p /" + pasta_des + "/" + pasta + " ; fi"
	print cmd
	subprocess.check_call(['ssh',usuario + "@" + ip_remoto,cmd])

def removeRemoteFolder(pasta_des, tamanho, usuario, ip_remoto):
	print "\nRemovendo a pasta remota\n"
	cmd = "rm -rf /" + pasta_des + "/" + tamanho
	subprocess.check_call(['ssh',usuario + "@" + ip_remoto,cmd])

def createLocalFolder(pasta_des, tipo, tamanho):
	print "\nCriando pasta local para recebimento de arquivos ...\n"
	cmd = "if [ ! -d " + " /" + pasta_des + "/" + tipo + "/" + tamanho + " ] ; then mkdir -p /" + pasta_des + "/" + tipo + "/" + tamanho + " ; fi"
	subprocess.check_call(cmd, shell=True)

def removeLocalFolder(pasta_des, tipo, tamanho):
	print "\nRemovendo arquivos e pasta local criadas para o recebimento ...\n"
	cmd = "rm -rf " + "/" + pasta_des + "/" + tipo + "/" + tamanho
	subprocess.check_call(cmd, shell=True)

def executeXrootD(usuario,ip_remoto,cmd):
	print "\nExecutando o XrootD\n"
	retorno = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
	#print retorno
	return retorno

def filterXrootD(resultado_xrootd):
	regex_velocidade = "[\d.]*[\w]*MB\/s"
	#print regex_velocidade
	lista_velocidade = re.findall(regex_velocidade,resultado_xrootd)
	#print lista_velocidade
	velocidade       = lista_velocidade[len(lista_velocidade) - 1]
	#velocidade       = velocidade.replace(" avg", "")
	velocidade 		 = "{0:0.1f}".format(convertToMb(velocidade))
	return velocidade

def saveXrootDResult(velocidade, cenario, erro, numero_teste):
 	s = xrootdData(velocidade=velocidade, scenario = cenario, descricao_erro = erro, num_teste = numero_teste)
	s.save()


def convertToMb(velocidade):
	numero = float(re.search('[\d.]*',velocidade).group(0))

	if velocidade[-6] == "G":
		numero = numero*1024
	elif velocidade[-6] == "k":
		numero = numero/1024

	if velocidade[-5] == "B":
		numero = numero*8

	return numero * 8

def xrootdTool(ip_remoto, tamanho, numero_teste, pasta_ori, pasta_des, fluxo, cenario):
	pasta_temp = 'area-teste'
	tipo     = "gridftp_ftp"
	usuario  = "sdmz"
	data     = time.strftime('%d/%m %H:%M:%S')
	porta    = "2811"
	pasta 	 = tamanho + "/" + str(fluxo)
	error_description = ''
	hostname 		= "sdmz@" + ip_remoto

	try:


		# iniciarXrootDRemoto(hostname, pasta_ori)

		removeLocalFile(pasta_des,tamanho)
		# createLocalFolder(pasta_des, tipo, tamanho)

		cmd_xrootd = "xrdcp xroot://sdmz@" + ip_remoto + "//" + pasta_ori + "/" + tamanho + "_file /" + pasta_des

		print cmd_xrootd

		retorno_xrootd = executeXrootD(usuario, ip_remoto, cmd_xrootd)
		# finalizarXrootDTRemoto(hostname)
		resultado_xrootd = filterXrootD(retorno_xrootd)
		#print resultado_xrootd
		# removeLocalFolder(pasta_des, tipo, tamanho)
		saveXrootDResult(resultado_xrootd, cenario, error_description, numero_teste)

	except Exception as e:
		error_description = e
		saveXrootDResult(0, cenario, error_description, numero_teste)
