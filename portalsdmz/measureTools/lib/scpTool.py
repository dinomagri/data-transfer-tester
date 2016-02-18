import subprocess, re, time
from measureTools.models import scpData

def createRemoteFolder(pasta_des, tipo, tamanho, usuario, ip_remoto):
	print "\nCriando pasta remota para envio de arquivos ...\n"
	cmd_ssh = "if [ ! -d " + " /" + pasta_des + "/" + tipo + "/" + tamanho + " ] ; then mkdir -p " + pasta_des + "/" + tipo + "/" + tamanho + " ; fi"
	subprocess.check_call(['ssh',usuario + "@" + ip_remoto,cmd_ssh])

def removeRemoteFolder(pasta_des, tipo, tamanho, usuario, ip_remoto):
	print "\nRemovendo o arquivo remoto\n"
	cmd_ssh = "rm -rf " + pasta_des + "/" +  tipo + "/" + tamanho 
	subprocess.check_call(['ssh',usuario + "@" + ip_remoto,cmd_ssh])

def executeScp(cmd):
	print "\nExecutando o scp\n"
	p = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
	return p

def filterResult(retorno_scp, tamanho):
	resultado = {'velocidade':0,'tempo':0}
	regex_tempo = '[\d.]{1,}'
	regex_linha_tempo = 'Transferred:[\w ,.]*'
	lista_tempo = re.findall(regex_linha_tempo,retorno_scp)
	resultado['tempo'] = re.findall(regex_tempo,lista_tempo[0])
	resultado['velocidade'] = "{0:0.1f}".format(convertBits(tamanho)/float(resultado['tempo'][-1]))
	return resultado

def convertBits(tamanho):
	if tamanho == '128M':
		return 128*8
	elif tamanho == '1G':
		return 1024*8
	elif tamanho == '10G':
		return 10240*8
	else:
		return 0

def saveScpResult(velocidade, cenario, erro, numero_teste):
 	s = scpData(velocidade = velocidade, scenario = cenario, descricao_erro = erro, num_teste = numero_teste)
	s.save()
	
def scpTool(ip_remoto, tamanho, numero_teste, pasta_ori, pasta_des, cenario):
	tipo     = "scp"
	usuario  = "sdmz"
	data     = time.strftime('%d/%m %H:%M:%S')
	descricao_erro = ''

	try:
		createRemoteFolder(pasta_des, tipo, tamanho, usuario, ip_remoto)


	#	cmd = "scp -v " + usuario + "@" + ip_remoto + ":" + pasta_des + "/" + tipo  + "/" + tamanho + "/" + tamanho + "_file " + "/"+ pasta_ori + "/" + tamanho + "_file_" + str(numero_teste)
	#	print cmd

		cmd = "scp -v " + " /"+ pasta_ori + "/" + tamanho + "_file " + usuario + "@" + ip_remoto + ":" + pasta_des + "/" + tipo  + "/" + tamanho + "/" + tamanho + "_file_" + str(numero_teste)
	
		retorno_scp = executeScp(cmd)
		resultado_scp = filterResult(retorno_scp, tamanho)
		removeRemoteFolder(pasta_des, tipo, tamanho, usuario, ip_remoto)
		saveScpResult(resultado_scp['velocidade'], cenario, descricao_erro, numero_teste)
	
	except Exception as e:
		descricao_erro = e
		saveScpResult(0, cenario, descricao_erro, numero_teste)
	
