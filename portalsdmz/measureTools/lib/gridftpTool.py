#!/usr/bin/python

import time, subprocess, re
from measureTools.models import gridftpData

def createRemoteFolder(pasta_des, pasta, usuario, ip_remoto):
	print "\nCriando pasta remota para envio de arquivos ...\n"
	cmd = "if [ ! -d " + "/" + pasta_des + "/" + pasta + " ] ; then mkdir -p /" + pasta_des + "/" + pasta + " ; fi"
	print cmd
	subprocess.check_call(['ssh',usuario + "@" + ip_remoto,cmd])	

def removeRemoteFolder(pasta_des, tamanho, usuario, ip_remoto):
	print "\nRemovendo a pasta remota\n"
	cmd = "rm -rf /" + pasta_des + "/" + tamanho
	subprocess.check_call(['ssh',usuario + "@" + ip_remoto,cmd])

def executeGridftp(usuario,ip_remoto,cmd):
	print "\nExecutando o gridftp\n"
	retorno = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
	return retorno

def filterGridftp(resultado_gridftp):
	regex_velocidade = "[\d.]* [\w]*\/sec avg"
	lista_velocidade = re.findall(regex_velocidade,resultado_gridftp)
	velocidade       = lista_velocidade[len(lista_velocidade) - 1]
	velocidade       = velocidade.replace(" avg", "")
	velocidade 		 = "{0:0.1f}".format(convertToMb(velocidade))
	return velocidade

def saveGridftpResult(velocidade, cenario, erro, numero_teste):
 	s = gridftpData(velocidade=velocidade, scenario = cenario, descricao_erro = erro, num_teste = numero_teste)
	s.save()

def convertToMb(velocidade):
	numero = float(re.search('[\d.]*',velocidade).group(0))
	
	if velocidade[-6] == "G":
		numero = numero*1024
	elif velocidade[-6] == "k":
		numero = numero/1024

	if velocidade[-5] == "B":
		numero = numero*8

	return numero

def gridftpTool(ip_remoto, tamanho, numero_teste, pasta_ori, pasta_des, fluxo, cenario):
	pasta_temp = 'area-teste'	
	tipo     = "gridftp_ftp"
	usuario  = "sdmz"
	data     = time.strftime('%d/%m %H:%M:%S')
	porta    = "2811"
	pasta 	 = tamanho + "/" + str(fluxo)
	error_description = ''

	try:
		createRemoteFolder(pasta_des, pasta, usuario, ip_remoto)
		cmd_gridftp = "time -p globus-url-copy -vb -p " + str(fluxo) + " ftp://" + ip_remoto + ":" + str(porta) + "/dados/" + pasta_temp  + "/" + tamanho + "_file file:///" + pasta_des + "/" + tamanho + "_file_" + str(numero_teste)
		
		print cmd_gridftp

		retorno_gridftp = executeGridftp(usuario, ip_remoto, cmd_gridftp)
		resultado_gridftp = filterGridftp(retorno_gridftp)
		removeRemoteFolder(pasta_des, tamanho, usuario, ip_remoto)
		saveGridftpResult(resultado_gridftp, cenario, error_description, numero_teste)

	except Exception as e:
		error_description = e
		saveGridftpResult(0, cenario, error_description, numero_teste)
