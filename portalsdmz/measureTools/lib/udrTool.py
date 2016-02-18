#!/usr/bin/python

import time, subprocess, re
from measureTools.models import udrData

def criar_pasta_remota(pasta_des, pasta, usuario, ip_remoto):
	print "Criando pasta remota para receber o arquivo..."
	cmd = "if [ ! -d " + pasta_des + "/" + pasta + \
		" ] ; then mkdir -p " + pasta_des + "/" + pasta + " ; fi"
	subprocess.check_call(['ssh',usuario + "@" + ip_remoto,cmd])

def remover_pasta_remota(pasta_des, tamanho, usuario, ip_remoto):
	print "Deletando pasta remota"
	cmd = "rm -rf " + pasta_des + "/" + tamanho
	subprocess.check_call(['ssh',usuario + "@" + ip_remoto,cmd])

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
		criar_pasta_remota(pasta_des, pasta, usuario, ip_remoto)

		#comando = 'udr rsync -av -stats --progress '+ usuario + '@' + ip_remoto + ":" + pasta_des + '/' + pasta + '/' + tamanho + '_file' + ' /' + pasta_ori + '/' + tamanho + '_file_' + str(numero_teste)


		#print comando

		comando = 'udr rsync -av -stats --progress ' + \
			"/" + pasta_ori + '/' + tamanho + '_file ' + usuario + '@' + ip_remoto + ':' + pasta_des + \
			 '/' + pasta + '/' + tamanho + '_file_' + str(numero_teste)
		
		print comando

		resultado_udr = executa_udr(comando);
		remover_pasta_remota(pasta_des, tamanho, usuario, ip_remoto)
		saveUdrResult(resultado_udr, numero_teste, cenario, erro)

	except Exception as e:
		erro = e
		saveUdrResult(0, numero_teste, cenario, erro)
