#!/usr/bin/python

import time, subprocess, re
from measureTools.models import udrData

def createLocalFolder(pasta_des, tipo, tamanho):
	print "\nCriando pasta local para recebimento de arquivos ...\n"
	cmd = "if [ ! -d " + " /" + pasta_des + "/" + tipo + "/" + tamanho + " ] ; then mkdir -p /" + pasta_des + "/" + tipo + "/" + tamanho + " ; fi"
	subprocess.check_call(cmd, shell=True)

def removeLocalFolder(pasta_des, tipo, tamanho):
	print "\nRemovendo arquivos e pasta local criadas para o recebimento ...\n"
	cmd = "rm -rf " + "/" + pasta_des + "/" + tipo + "/" + tamanho
	subprocess.check_call(cmd, shell=True)

def executa_udr(comando):
	print "Executando o UDR"
	resultado = subprocess.check_output(comando, shell=True)
	velocidade = parse_resultado(resultado)
	return velocidade

def parse_resultado(resultado):
	regexVelocidade = "[\d.]+[\w]+/s"
	lista_velocidade = re.findall(regexVelocidade, resultado)
	velocidade = conversor_byte_bits(lista_velocidade[-1])
	return velocidade

def conversor_byte_bits(velocidade):
	regexVelocidade = "[\d.]+"
	numero = float(re.findall(regexVelocidade,velocidade)[0])

	if (re.search('KB',velocidade)):
		return numero/128
	elif (re.search('MB',velocidade)):
		return numero*8
	elif (re.search('GB',velocidade)):
		return numero*1024*8
	else:
		return 0

def saveUdrResult(velocidade,numero_teste, cenario, erro):
 	s = udrData(velocidade=velocidade, scenario = cenario, num_teste = numero_teste, descricao_erro = erro)
	s.save()

def udrTool(ip_remoto, tamanho, numero_teste, pasta_ori, pasta_des, fluxo, cenario):

	#pasta_temp = 'area-dados'
	tipo 	 = 'udr'
	usuario  = "sdmz"
	data     = time.strftime('%d/%m %H:%M:%S')
	erro 	 = ''

	pasta 	 = tamanho + "/" + str(fluxo)

	print ""
	print "---------------"
	print "----- UDR -----"
	print "---------------"
	print ""

	try:
		createLocalFolder(pasta_des, tipo, tamanho)

		comando = 'udr rsync -av -stats --progress ' + usuario + '@' + ip_remoto + ":/" + pasta_ori + '/' + tamanho + '_file ' + '/' + pasta_des + '/' + tipo + "/" + tamanho + "/" + tamanho + "_file_" + str(numero_teste)
		
		resultado_udr = executa_udr(comando);
		removeLocalFolder(pasta_des, tipo, tamanho)
		saveUdrResult(resultado_udr, numero_teste, cenario, erro)

	except Exception as e:
		erro = e
		saveUdrResult(0, numero_teste, cenario, erro)
