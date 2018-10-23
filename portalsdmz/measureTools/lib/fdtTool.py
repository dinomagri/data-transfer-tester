#!/usr/bin/python

import time, subprocess, re
from measureTools.models import fdtData

def iniciarFDTRemoto(hostname):
	print "\nIniciando fdt server remoto ...\n"
	subprocess.Popen(['ssh', hostname, 'java -jar /home/sdmz/fdt.jar -S'])
	subprocess.call(['sleep', '2'])
	print"\n\n"

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

def executeFdT(usuario,ip_remoto,cmd):
	print "\nExecutando o FDT\n"
	retorno = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
	return retorno

def filterFdT(resultado_fdt,tamanho):
	regex_velocidade = "\d+s"
	lista_velocidade = re.findall(regex_velocidade,resultado_fdt)
        print lista_velocidade
    #regex = "\d+"
	#lista = re.findall(regex,lista_velocidade)
	velocidade = lista_velocidade[len(lista_velocidade) - 1]
        print velocidade
        x = velocidade.split("s")

        y = x[0]
        print y
        if tamanho == "1G":
            vel = 1024 / int(y)
				velf = vel * 8
        elif tamanho == "10G":
            vel = 10024 / int(y)
        elif tamanho == "100G":
            vel = 100024 / int(y)

        print velf
	return  velf

def saveFdTResult(velocidade, cenario, erro, numero_teste):
 	s = fdtData(velocidade=velocidade, scenario = cenario, descricao_erro = erro, num_teste = numero_teste)
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

def fdtTool(ip_remoto, tamanho, numero_teste, pasta_ori, pasta_des, fluxo, cenario):
	pasta_temp = 'area-teste'
	tipo     = "fdt_ftp"
	usuario  = "sdmz"
	data     = time.strftime('%d/%m %H:%M:%S')
	porta    = "2811"
	pasta 	 = tamanho + "/" + str(fluxo)
	error_description = ''

	try:
		createLocalFolder(pasta_des, tipo, tamanho)
		#cmd_xrootd = "xrdcp -d 3 ftp/test6 root://192.168.122.187//root/FTP/ xrdcp /root/Ftp/test9 test9 -d1"
		#iniciarFDTRemoto(ip_remoto)
		subprocess.call(['sleep', '10'])
		#cmd_xrootd = "xrdcp -d 3 "+ pasta_ori  + "/" + tamanho +"  root://" + ip_remoto + " xrdcp   /root/"+ pasta_des + "/" + tipo + "/" + tamanho + "_file_" + str(numero_teste) + " -d1 "
		#cmd_xrootd = "time -p globus-url-copy -vb -p " + str(fluxo) + " ftp://" + ip_remoto + ":" + str(porta)  + "/" + pasta_ori  + "/" + tamanho + "_file file:///" \
		#	+ pasta_des + "/" + tipo + "/" + tamanho + "_file_" + str(numero_teste)
		cmd_fdt = "java -jar /home/admin/fdt.jar -c "+ ip_remoto  +" -d /"+ pasta_des +" /home/admin"+ pasta_ori + tamanho +"_file"

		print cmd_fdt

		retorno_fdt = executeFdT(usuario, ip_remoto, cmd_fdt)
		resultado_fdt = filterFdT(retorno_fdt,tamanho)
		removeLocalFolder(pasta_des, tipo, tamanho)
		saveFdTResult(resultado_fdt, cenario, error_description, numero_teste)

	except Exception as e:
		error_description = e
		saveFdTResult(0, cenario, error_description, numero_teste)
