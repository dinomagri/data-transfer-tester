#!/usr/bin/python

import time, subprocess, re, os
from measureTools.models import aria2cData

def criar_pasta_local(pasta_des, pasta):
	print "Criando pasta local para receber o arquivo..."
	cmd = "if [ ! -d " + "/" + pasta_des + "/" + pasta + \
		" ] ; then mkdir -p " + "/" + pasta_des + "/" + pasta + " ; fi"
	subprocess.check_call(cmd, shell=True)

def remover_pasta_local(pasta_des, tamanho):
	print "Deletando pasta local"
	cmd = "rm -rf " + "/" + pasta_des + "/" + tamanho
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
	
	pasta_temp = "area-teste"
	tipo = 'aria2c'
	usuario  = "root"
	data     = time.strftime('%d/%m %H:%M:%S')
	erro 	 = ''
	work_dir = os.getcwd()
	pasta = tamanho + "/" + str(fluxo)

	# programa
	print ""
	print "---------------"
	print "--- Aria2c ----"
	print "---------------"
	print ""

	try:
		os.chdir(os.path.abspath(os.sep))
		criar_pasta_local(pasta_des, pasta)

		comando = "aria2c " + "ftp://" + ip_remoto + "/" + pasta_temp + "/" + tamanho + "_file -d /" + pasta_des + "/" + pasta

		#comando = 'aria2c -d ' + "/" + pasta_des + '/' + pasta + ' -x ' + \
		#	 str(fluxo) + ' ftp://' + ip_remoto + \
		#	 '/' + tamanho + '_file'
		resultado_aria2c = executa_aria2c(comando);
		remover_pasta_local(pasta_des, tamanho)
		os.chdir(work_dir)
		saveAria2cResult(resultado_aria2c, numero_teste, cenario, erro)

	except Exception as e:
		erro = e
		saveAria2cResult(0, numero_teste, cenario, erro)
		os.chdir(work_dir)
