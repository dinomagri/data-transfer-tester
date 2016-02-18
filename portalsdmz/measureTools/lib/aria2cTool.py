#!/usr/bin/python

import time, subprocess, re, os
from measureTools.models import aria2cData

def createLocalFolder(pasta_des, tipo, tamanho):
	print "\nCriando pasta local para recebimento de arquivos ...\n"
	cmd = "if [ ! -d " + " /" + pasta_des + "/" + tipo + "/" + tamanho + " ] ; then mkdir -p /" + pasta_des + "/" + tipo + "/" + tamanho + " ; fi"
	subprocess.check_call(cmd, shell=True)

def removeLocalFolder(pasta_des, tipo, tamanho):
	print "\nRemovendo arquivos e pasta local criadas para o recebimento ...\n"
	cmd = "rm -rf " + "/" + pasta_des + "/" + tipo + "/" + tamanho
	subprocess.check_call(cmd, shell=True)

def executa_aria2c(comando):
	resultado = subprocess.check_output(comando, shell=True)
	velocidade = parse_resultado(resultado)
	return velocidade

def parse_resultado(resultado):
	regexVelocidade = "[\w]+\/s"
	lista_velocidade = re.findall(regexVelocidade, resultado)
	velocidade = conversor_byte_bits(lista_velocidade[0])
	return velocidade

def conversor_byte_bits(velocidade):
	regexVelocidade = "[\d]+"
	numero = float(re.findall(regexVelocidade,velocidade)[0])

	if (re.search('KiB',velocidade)):
		return numero/128
	elif (re.search('MiB',velocidade)):
		return numero*8
	elif (re.search('GiB',velocidade)):
		return numero*1024*8
	else:
		return 'erro'

def saveAria2cResult(velocidade, numero_teste, cenario, erro):
 	s = aria2cData(velocidade=velocidade, num_teste = numero_teste, scenario = cenario, descricao_erro = erro)
	s.save()

def aria2cTool(ip_remoto, tamanho, numero_teste, pasta_ori, pasta_des, fluxo, cenario):
	# esta fazendo o download em vez de upload
	
	tipo = 'aria2c'
	data     = time.strftime('%d/%m %H:%M:%S')
	erro 	 = ''
	work_dir = os.getcwd()
	
	try:
		#os.chdir(os.path.abspath(os.sep))
		createLocalFolder(pasta_des, tipo, tamanho)

		comando = "aria2c " + "-x" + str(fluxo) + " ftp://" + ip_remoto + "/" + tamanho + "_file -d /" + pasta_des + "/" + tipo + "/" + tamanho + "/" + tamanho + "_file_" + str(numero_teste) 
		print ">>>>>>>>>>>>>>>>>"
		print comando
		resultado_aria2c = executa_aria2c(comando);
		removeLocalFolder(pasta_des, tipo, tamanho)
		os.chdir(work_dir)
		saveAria2cResult(resultado_aria2c, numero_teste, cenario, erro)

	except Exception as e:
		erro = e
		saveAria2cResult(0, numero_teste, cenario, erro)
		os.chdir(work_dir)
