import subprocess, os, re, shutil, time
from measureTools.models import wgetData


def createLocalFolder(pasta_des, tipo, tamanho):
	print "\nCriando pasta local para recebimento de arquivos ...\n"
	cmd = "if [ ! -d " + " /" + pasta_des + "/" + tipo + "/" + tamanho + " ] ; then mkdir -p /" + pasta_des + "/" + tipo + "/" + tamanho + " ; fi"
	subprocess.check_call(cmd, shell=True)

def removeLocalFolder(pasta_des, tipo, tamanho):
	print "\nRemovendo arquivos e pasta local criadas para o recebimento ...\n"
	cmd = "rm -rf " + "/" + pasta_des + "/" + tipo + "/" + tamanho
	subprocess.check_call(cmd, shell=True)


def executaWget(cmd):
	wget = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout = []
	while True:
		line = wget.stdout.readline()
		stdout.append(line)
		if line == '' and wget.poll != None:
			break
	return stdout

def regex_na_linha(linha, regex):
	output = re.search(regex, linha)
	if output:
		return output.group(0)
	else:
		return "--"

def remove_arquivo(caminho_arquivo) :

	if os.path.isdir(caminho_arquivo):
		try:
			shutil.rmtree(caminho_arquivo)
			return True
		except:
			print "Nao foi possivel remover o diretorio " + caminho_arquivo
			return False
	else :
		try:
			shutil.rmtree(caminho_arquivo)
			return True
		except:
			print "Nao foi possivel remover o arquivo " + caminho_arquivo
			return False

def converte_byte_bit(speed_byte) :

	speed_bit = re.search('\d+(,||.)\d+', speed_byte)

	if speed_bit:
		speed_bit = speed_bit.group(0)

		speed_bit = speed_bit.replace(',', '.')

		speed_bit = float(speed_bit) * 8.0

		return speed_bit
	else :
		print 'Erro na conversao de byte para bit'
		return 0.0

def saveWgetResults(velocidade,numero_teste, cenario, descricao_erro):
	s = wgetData(velocidade = velocidade, scenario=cenario, num_teste = numero_teste, descricao_erro = descricao_erro)
	s.save()

def wgetTool(ip_remoto, tamanho, numero_teste, pasta_destino, cenario):

	pasta_temp = "area-teste"
	user = "sdmz"
	tipo = "wget"
	data = time.strftime('%d/%m %H:%M:%S')
	descricao_erro = ''

	pasta = tamanho

	"""host_name = user + "@" + ip_remoto
	ssh_mkdir = "if [ ! -d " + " /" + pasta_destino + "/" + pasta + " ] ; then mkdir -p " + pasta_destino + "/" + pasta + " ; fi"

	try: 
		ssh = subprocess.Popen(['ssh', host_name, ssh_mkdir])
		ssh.communicate()
	except subprocess.CalledProcessError:
		descricao_erro = subprocess.CalledProcessError
		
	if not os.path.isdir("/" +pasta_destino + "/" + pasta) :
		os.makedirs("/" + pasta_destino + "/" + pasta)
	"""

	createLocalFolder(pasta_destino, tipo, tamanho)

	print "iniciando copia =", numero_teste

	cmd = 'wget' + " ftp://" + ip_remoto + "/" + tamanho + "_file -O" + " /" + pasta_destino + "/" + tipo + "/" + tamanho + "/" + tamanho + "_file_" + str(numero_teste) + " -m"
	
#	cmd = 'wget -O' + " /"+pasta_destino+"/"+pasta+"/"+tamanho+"_file_"+str(numero_teste) + " -m ftp://" + ip_remoto + "/" + tamanho + "_file"

	print cmd
	lista_linhas = []

	lista_linhas = executaWget(cmd)
	if len(lista_linhas) <= 2:
		descricao_erro = 'erro na execucao do Wget'

	else:
		linha_velocidade = lista_linhas[-2]

		regex_velocidade = '\d+(,||.)\d+ \w+\/s'
		velocidade = regex_na_linha(linha_velocidade, regex_velocidade)
		velocidade = "{0:0.1f}".format(converte_byte_bit(velocidade))

		print "Removendo os arquivos auxiliares"

		#remove_arquivo(ip_remoto + "/")
		removeLocalFolder(pasta_destino, tipo, tamanho)

		saveWgetResults(velocidade,numero_teste, cenario, descricao_erro)
