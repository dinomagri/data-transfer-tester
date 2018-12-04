# data-transfer-tester

O programa [Science DMZ da RNP](https://wiki.rnp.br/display/sciencedmz/Science+DMZ+Home) visa estudar e disseminar melhores práticas de infraestrutura de redes de campus voltadas às aplicações científicas. Dada a crescente escala em que volumes cada vez maiores de dados precisam ser processados e analisados por aplicações científicas as redes de campus das universidades necessitam se adequar a esta nova demanda de transferência de dados entre laboratórios e instituições.

O **Data Transfer Tester** (DTT) foi desenvolvido para facilitar os testes de validação da máquina de transferência de dados ([DTN](https://wiki.rnp.br/display/sciencedmz/DTN)). As ferramentas disponíveis são:

* scp
* gridFTP
* iperf3
* udr
* axel
* aria2c
* wget
* XrootD
* FDT

Todas as ferramentas realizam o **Download dos dados**. Ou seja, onde o DTT estiver rodando, os dados serão baixados para essa máquina.


> Este software está em versão Beta. NÃO utilize em ambientes de produção!!!
---



## Licença

Veja arquivo LICENSE

## Autores

- Dino Magri
- Fabio Chu
- Felipe Waku
- Rodrigo Tejos

## Instalação e Configuração do CentOS 7 e das Ferramentas de Transferência

Para rodar é necessário que o host remoto e o DTT tenham essas ferramentas instaladas. Abaixo segue os tutoriais para instalação e configuração, tanto do sistema operacional CentOS 7 como também do DTN:

* Para a instalação do CentOS 7 -
  * Crie uma partição /dados com o sistema de arquivos XFS para facilitar os testes!!!
* Para a instalação e configuração básica do DTN -
* Para a instalação das ferramentas:
  * Instalação Globus Toolkit -
  * Instalação SCP/SSH HPN - 
  * Instalação UDR - 
  * Instalação aria2 - 
  * Instalação axel - 
  * Instalação XRootD -
  * Instalação FDT -

O DTT foi testado em ambiente CentOS 7 com as respectivas versões das ferramentas:

* scp - 
* scp hpn - 
* gridFTP - https://wiki.rnp.br/pages/viewpage.action?pageId=93327982
* iperf3 - 
* udr e rsync - https://wiki.rnp.br/pages/viewpage.action?pageId=88111586
* axel - https://wiki.rnp.br/pages/viewpage.action?pageId=89125404
* aria2c - https://wiki.rnp.br/pages/viewpage.action?pageId=89125400
* wget -
* xrootd - https://wiki.rnp.br/display/sciencedmz/XrootD
* fdt - https://wiki.rnp.br/display/sciencedmz/FDT

> Com um pouco de esforço, acredito que seja possível rodar o DTT em outras distribuições Linux.

### Instalação das depêndencias necessárias

Para instalar corretamente o software, será necessário instalar os seguintes softwares no Centos 7

```bash
sudo yum groupinstall "Development tools" -y
sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel -y
```



### Copiando o código fonte do DTT

Primeiro vamos realizar o download do código fonte:

```
cd ~
wget https://github.com/larc-usp/data-transfer-tester/archive/master.zip
unzip master.zip
rm -rf master.zip
cd data-transfer-tester-master/
```

* Se tudo estiver certo, agora podemos prosseguir com a instalação do virtualenv onde o DTT irá rodar isoladamente. Mais sobre virtualenv em https://virtualenv.readthedocs.org/en/latest/

```sudo yum install python-virtualenv -y```

Para iniciar um ambiente virtual e ativá-lo:

```
virtualenv -p /usr/local/bin/python2.7 venv
source venv/bin/activate
```
> Note que estamos dentro da pasta data-transfer-tester

Rode o comando ```python``` e verifique se a versão é a 2.7.

> Obs: Todas as bibliotecas que forem instaladas nesse ambiente virtual através do comando pip, afetará apenas este ambiente virtual. Para desativar o virtualenv, utilize na pasta raiz o comando ```deactivate```.


### Instalando as bibliotecas do DTT

Para rodar o DTT, é necessário instalar as seguintes depêndencias:

```bash
Django==1.8.4
django-chartit==0.1
gevent==1.0.1
greenlet==0.4.6
pysqlite==2.6.3
simplejson==3.6.5
whichcraft==0.4.1
```

Para instalar essas bibliotecas, vamos utilizar o pip com o parâmetro -r para instalar todas as bibliotecas listadas no arquito requirements.txt

```bash
pip install -r requirements.txt
```

### Rodando o DTT pela primeira vez

Se tudo estiver ok, acesse a pasta portalsdmz e rode o comando:

```bash
cd portalsdmz
rm db.sqlite3
python manage.py migrate
python manage.py runserver 172.20.5.170:8000
```

> Utilize o IP que está configurado para a máquina DTT.

**IMPORTANTE** - Caso a variável DJANGO_SETTINGS_MODULE está definida no ambiente, será necessário remove-la antes de rodar os comandos acima, pois o mesmo irá gerar um erro.

```bash
unset DJANGO_SETTINGS_MODULE
```

Agora vamos criar um usuário admin para a seção de Administração do portal (/admin), digite no terminal Ctrl+C para parar a execução do DTT e digite:

```bash
python manage.py createsuperuser
```

Escolha o login e senha e inicie o servidor novamente com o comando:

```bash
python manage.py runserver 172.20.5.170:8000
```

Acesse o navegador, digite: http://172.20.5.170:8000 e tente realizar o login.

> Lembre-se: O IP acima deve ser trocado para o IP correspondente da máquina onde o DTT está instalado.


### Testando

Caso os arquivos de teste estejam criados, utilize o Portal DTT para criar um novo cenário de teste e iniciar as transferências.

O DTT utiliza 3 tamanhos de arquivos diferentes para realizar os teste (1G, 10G e 100G) e os mesmos devem ser criados no diretório /dados/area-teste. O comando para criar esses arquivos são:

* Para criar o arquivo de 1G_file - ```dd if=/dev/zero of=/dados/area-teste/1G_file bs=4k count=250000```
* Para criar o arquivo de 10G_file - ```dd if=/dev/zero of=/dados/area-teste/10G_file bs=4k count=2500000```
* Para criar o arquivo de 100G_file - ```dd if=/dev/zero of=/dados/area-teste/100G_file bs=4k count=25000000```

Para testar manualmente as ferramentas para verificar se tudo está funcionando corretamente:

> O IP abaixo, deve ser trocado pelo IP do host remoto.

* scp
	* ```scp sdmz@172.20.5.38:/dados/area-teste/1G_file /dados/area-teste/1G_file```

* gridFTP
	* No host remoto: ```globus-gridftp-server -aa &```
	* Na máquina DTT: ```globus-url-copy -vb -p 1 ftp://172.20.5.38:2811/dados/area-teste/1G_file file:///dados/area-teste/1G_file```

* iperf3
	* No host remoto: ```iperf3 -s &```
	* Na máquina DTT: ```iperf3 -c 172.20.5.38 -P 1 -i1 -O 5 -n 1G```

* udr
	* ```udr rsync -av -stats --progress sdmz@172.20.5.38:/dados/area-teste/1G_file /dados/area-teste/1G_file```

Para as ferramentas wget, axel e aria2c é necessário ter um servidor FTP rodando no host remoto - https://wiki.rnp.br/pages/viewpage.action?pageId=89564070#InstalaçãoeconfiguraçãobásicadoDTN-ServidorFTP

* wget
	* ```wget ftp://172.20.5.38/1G_file -O /dados/area-teste/1G_file```

* axel
	* ```axel ftp://172.20.5.38/1G_file -o /dados/area-teste/1G_file -n 1```

* aria2c
	* ```aria2c -x1 ftp://172.20.5.38/1G_file -d /dados/area-teste/1G_file```

Para maiores informações sobre o uso das ferramentas de transferência acesse - https://wiki.rnp.br/pages/viewpage.action?pageId=89564131

Se nenhum das execuções das ferramentas de transferência apresentou erro, podemos adicionar um novo Cenário de Teste através do Portal do Data Transfer Tester (DTT).

Acesse: http://172.20.5.170:8000, realize o login, crie um ***Novo cenário*** e inicie a transferência.

Para acessar a área administrativa: http://172.20.5.170:8000

> Lembre-se: O IP acima deve ser trocado para o IP correspondente da máquina onde o DTT está instalado.
