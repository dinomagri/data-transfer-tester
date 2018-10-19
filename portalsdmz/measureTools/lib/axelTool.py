#!/usr/bin/python

import time, subprocess, re, os
from measureTools.models import axelData

def createLocalFolder(pasta_des, tipo, tamanho):
	print "\nCriando pasta local para recebimento de arquivos ...\n"
	cmd = "if [ ! -d " + " /" + pasta_des + "/" + tipo + "/" + tamanho + " ] ; then mkdir -p /" + pasta_des + "/" + tipo + "/" + tamanho + " ; fi"
	subprocess.check_call(cmd, shell=True)

def removeLocalFolder(pasta_des, tipo, tamanho):
	print "\nRemovendo arquivos e pasta local criadas para o recebimento ...\n"
	cmd = "rm -rf " + "/" + pasta_des + "/" + tipo + "/" + tamanho
	subprocess.check_call(cmd, shell=True)

"""
def criar_pasta_local(pasta_des, pasta):
	print "Criando pasta local para receber o arquivo..."
	cmd = "if [ ! -d " + "/" + pasta_des + "/" + pasta + \
		" ] ; then mkdir -p " + "/" + pasta_des + "/" + pasta + " ; fi"
	subprocess.check_call(cmd, shell=True)

def remover_pasta_local(pasta_des, tamanho):
	print "Deletando pasta local"
	cmd = "rm -rf /" + pasta_des + "/" + tamanho
	subprocess.check_call(cmd, shell=True)

"""

def executa_axel(comando):
	resultado = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT)
	velocidade = parse_resultado(resultado)
	return velocidade

def parse_resultado(resultado):
	regexVelocidade = "[\d.,]+ [\w]+/s"
	lista_velocidade = re.findall(regexVelocidade, resultado)
	velocidade = conversor_byte_bits(lista_velocidade[0])
	return velocidade

def conversor_byte_bits(velocidade):
	regexVelocidade = "[\d]+"
	numero = float(re.findall(regexVelocidade,velocidade)[0].replace(",", "."))

	if (re.search('KB',velocidade)):
		return numero/128
	elif (re.search('MB',velocidade)):
		return numero*8
	elif (re.search('GB',velocidade)):
		return numero*1024*8
	else:
		return 'erro'

def saveAxelResult(velocidade, numero_teste,cenario, erro):
 	s = axelData(velocidade=velocidade, scenario = cenario, num_teste = numero_teste, descricao_erro = erro)
	s.save()

def axelTool(ip_remoto, tamanho, numero_teste, pasta_ori, pasta_des, fluxo, cenario):
	# esta fazendo o download em vez de upload

	tipo 	 = 'axel'
	usuario  = "sdmz"
	data     = time.strftime('%d/%m %H:%M:%S')
	erro 	 = ''

	work_dir = os.getcwd()
	pasta = tamanho + "/" + str(fluxo)

	try:
		#os.chdir(os.path.abspath(os.sep))
		createLocalFolder(pasta_des, tipo, tamanho)
		print 'pasta criada'

		comando = 'axel ftp://' + ip_remoto + '/pub/' + tamanho + '_file -o /' + pasta_des + "/" + tipo + "/" + tamanho + "/" + tamanho + "_file_" + str(numero_teste) + " -n " + str(fluxo)

		print comando

		resultado_axel = executa_axel(comando)
		removeLocalFolder(pasta_des, tipo, tamanho)
		os.chdir(work_dir)
		saveAxelResult(resultado_axel, numero_teste, cenario, erro)

	except Exception as e:
		os.chdir(work_dir)
		erro = e
		saveAxelResult(0,numero_teste,cenario, erro)
