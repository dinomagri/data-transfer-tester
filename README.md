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

Todas as ferramentas realizam o Download dos dados. Ou seja, onde o DTT estiver rodando, os dados serão baixados para essa máquina.


> Este software está em versão Alpha. NÃO utilize em ambientes de produção!!!
---



## Licença

Veja arquivo LICENSE

## Autores

- Dino Magri
- Fabio Chu
- Felipe Waku



## Instalação e Configuração do CentOS 6.7 e das Ferramentas de Transferência

Para rodar é necessário que o host remoto e o DTT tenham essas ferramentas instaladas. Abaixo segue os tutoriais para instalação e configuração, tanto do sistema operacional CentOS 6.7 como também do DTN:

* Para a instalação do CentOS 6.7 - https://wiki.rnp.br/pages/viewpage.action?pageId=89563937
* Para a instalação e configuração básica do DTN - https://wiki.rnp.br/pages/viewpage.action?pageId=89564070
* Para a instalação das ferramentas:
	* Instalação Globus Toolkit 5.2 - https://wiki.rnp.br/pages/viewpage.action?pageId=89564077
	* Instalação SCP/SSH HPN - https://wiki.rnp.br/pages/viewpage.action?pageId=88110308
	* Instalação UDR - https://wiki.rnp.br/pages/viewpage.action?pageId=88111586
	* Instalação aria2 - https://wiki.rnp.br/pages/viewpage.action?pageId=89125400
	* Instalação axel - https://wiki.rnp.br/pages/viewpage.action?pageId=89125404

O DTT foi testado em ambiente CentOS 6.7 com as respectivas versões das ferramentas:

* scp - ```OpenSSH_5.3p1, OpenSSL 1.0.1e-fips 11 Feb 2013```
* scp hpn - ```OpenSSH_6.6p1-hpn14v5, OpenSSL 1.0.1e-fips 11 Feb 2013```
* gridFTP - ```globus-url-copy: 8.6``` - Já vem com o globus Toolkit 5.2
* iperf3 - ```iperf 3.1.2```
* udr e rsync - ```UDR version v0.9.4-10-g7638b30``` e ```rsync  version 3.0.6  protocol version 30```
* axel - ```Axel version 2.4 (Linux)```
* aria2c - ```aria2 versão 1.16.4```
* wget - ```GNU Wget 1.12 construído em linux-gnu.```

> Com um pouco de esforço, acredito que seja possível rodar o DTT em outras distribuições Linux.

## Instalação do DTT

Antes de rodar o DTT, é necessário instalar a versão 2.7 do Python, pois é necessário manter a versão 2.6 que é utilizada pelo CentOs 6.7. Portanto é importante que ambas as versões (2.6 e 2.7) existam, uma vez que o sistema operacional pode quebrar.

Na página: https://github.com/h2oai/h2o-2/wiki/Installing-python-2.7-on-centos-6.3.-Follow-this-sequence-exactly-for-centos-machine-only tem um passo a passo bem detalhado para instalar a versão 2.7 do Python no CentOS 6.3. Vale a leitura.

Para instalar a versão 2.7.11 no CentOS 6.7, devemos realizar os seguintes passos:

### Download, compilação e instalação

* Instalando as dependências:

```bash
sudo yum groupinstall "Development tools"
sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel -y
```

* Realizando o download, compilação e instalação do Python 2.7.11

```bash
cd /tmp
wget --no-check-certificate https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tar.xz
tar xf Python-2.7.11.tar.xz
cd Python-2.7.11/
./configure --prefix=/usr/local
make && sudo make altinstall
```

* Se nenhum erro aparecer, ditige no terminal:
	* Para verificar se a versão é a 2.6.6: ```python``` 
	* Para verificar se a versão é a 2.7.11: ```python2.7``` 


### Copiando o código fonte

Primeiro vamos realizar o download do código fonte, clonando o repositório do github:

```
cd ~ 
git clone git@github.com:dinomagri/data-transfer-tester.git
cd data-transfer-tester/
```

* Se tudo estiver certo, agora podemos prosseguir com a instalação do virtualenv onde o DTT irá rodar isoladamente. Mais sobre virtualenv em https://virtualenv.readthedocs.org/en/latest/

```sudo yum install python-virtualenv```

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
wsgiref==0.1.2
```

Para instalar essas bibliotecas, vamos utilizar o pip com o parâmetro -r para instalar todas as bibliotecas listadas no arquito requirements.txt

```bash
pip install -r requirements.txt
```

### Rodando o DTT pela primeira vez

Se tudo estiver ok, acesse a pasta portalsdmz e rode o comando:

```bash
rm db.sqlite3 
python manage.py migrate
python manage.py runserver 172.20.5.170:8000
```

> Utilize o IP que está configurado para a máquina DTT.

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

O DTT utiliza 3 tamanhos de arquivos diferentes para realizar os teste (1G, 10G e 100G) e os mesmos devem ser criados no diretório /dados. O comando para criar esses arquivos são:

* Para criar o arquivo de 1G_file - ```dd if=/dev/zero of=/dados/1G_file bs=4k count=250000```
* Para criar o arquivo de 10G_file - ```dd if=/dev/zero of=/dados/10G_file bs=4k count=2500000```
* Para criar o arquivo de 100G_file - ```dd if=/dev/zero of=/dados/100G_file bs=4k count=25000000```

Para testar manualmente as ferramentas para verificar se tudo está funcionando corretamente:

> O IP abaixo, deve ser trocado pelo IP do host remoto.

* scp 
	* ```scp sdmz@172.20.5.38:/dados/1G_file /dados/area-teste/1G_file```

* gridFTP
	* No host remoto: ```globus-gridftp-server -aa```
	* Na máquina DTT: ```globus-url-copy -vb -p 1 ftp://172.20.5.38:2811/dados/1G_file file:///dados/area-teste/1G_file```

* iperf3
	* No host remoto: ```iperf3 -s```
	* Na máquina DTT: ```iperf3 -c 172.20.5.38 -P 1 -i1 -O 5 -n 1G```

* udr
	* ```udr rsync -av -stats --progress sdmz@172.20.5.38:/dados/1G_file /dados/area-teste/1G_file```

Para as ferramentas wget, axel e aria2c é necessário ter um servidor FTP rodando no host remoto - https://wiki.rnp.br/pages/viewpage.action?pageId=89564070#InstalaçãoeconfiguraçãobásicadoDTN-ServidorFTP

* wget
	* ```wget ftp://172.20.5.38/1G_file -O /dados/area-teste/1G_file```

* axel
	* ```axel ftp://172.20.5.38/100G_file -o /dados/area-teste/100G_file -n 1```

* aria2c
	* ```aria2c -x1 ftp://172.20.5.38/1G_file -d /dados/area-teste/1G_file```

Para maiores informações sobre o uso das ferramentas de transferência acesse - https://wiki.rnp.br/pages/viewpage.action?pageId=89564131

Se nenhum das execuções das ferramentas de transferência apresentou erro, podemos adicionar um novo Cenário de Teste através do Portal do Data Transfer Tester (DTT).

Acesse: http://172.20.5.170:8000, realize o login, crie um ***Novo cenário*** e inicie a transferência.

Para acessar a área administrativa: http://172.20.5.170:8000

> Lembre-se: O IP acima deve ser trocado para o IP correspondente da máquina onde o DTT está instalado.