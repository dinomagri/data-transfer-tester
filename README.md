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

Este software está em versão Alpha, utilize por sua conta e risco.

## Instalação

Antes de rodar o DTT, é necessário atualizar o Python para a versão 2.7, pois o CentOS 6.7 mantem a versão 2.6. É importante que ambas as versões (2.6 e 2.7) existam.

Na página: https://github.com/h2oai/h2o-2/wiki/Installing-python-2.7-on-centos-6.3.-Follow-this-sequence-exactly-for-centos-machine-only tem um passo a passo bem detalhado para instalar a versão 2.7 no CentOS 6.3. Antes de iniciar os passos abaixo, leia o link acima.



Os passos abaixo, são para instalar a versão 2.7.11 no CentOS 6.7. Para realizar o Download, a compilação e a instalação execute:

```bash
sudo yum groupinstall "Development tools"
sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel -y

cd /tmp
wget --no-check-certificate https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tar.xz
tar xf Python-2.7.11.tar.xz
cd Python-2.7.11/
./configure --prefix=/usr/local
make && sudo make altinstall
```

Digite o terminal:

```python``` para verificar se a versão é a 2.6.6
```python2.7``` para verificar se a versão é a 2.7.11.


Se tudo estiver certo, agora podemos prosseguir com a instalação do virtualenv para inicial o Deploy da Aplicação.


[] Migrar para o Download do ZIP
Primeiro vamos realizar o Download do clonar o repositório do github:
```
cd ~ 
git clone git@github.com:dinomagri/data-transfer-tester.git
cd data-transfer-tester/
```
Agora vamos instalar o virtualenv para termos um ambiente isolado. Veja mais em [] Adicionar link.

```sudo yum install python-virtualenv```

Para iniciar um ambiente virtual e ativá-lo:

```
virtualenv -p /usr/local/bin/python2.7 venv
source venv/bin/activate
``` 

Assim toda a instalação que realizar utilizando o pip, afetará apenas esse ambiente virtual. Para desativar, utilize na pasta raiz o comando ```deactivate```.

As dependências para a instalação são:

```bash
Django==1.8.4
django-chartit==0.1
gevent==1.0.1
greenlet==0.4.6
pysqlite==2.6.3
simplejson==3.6.5
wsgiref==0.1.2
```

Para instalar utilize o pip

```
pip install -r requirements.txt
```


