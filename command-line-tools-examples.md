# Exemplos de linha de comando das ferramentas


## Copiar do DTN RNP para DTN USP

### SCP

```scp sdmz@dtn.sdmz.rnp.br:/dados/area-teste/1G_file /dados/area-teste/1G_file```

### GridFTP

* Servidor: 
```globus-gridftp-server -aa &```

* Cliente:

```globus-url-copy -vb -p 1 ftp://dtn.sdmz.rnp.br:2811/dados/area-teste/1G_file file:///dados/area-teste/1G_file```

### Iperf3

* Servidor
```iperf3 -s &```

* Cliente
```perf3 -c dtn.sdmz.rnp.br -P 1 -i1 -O 5 -n 1G```

### UDR
```udr rsync -av -stats --progress sdmz@dtn.sdmz.rnp.br:/dados/area-teste/1G_file /dados/area-teste/1G_file```

### Wget
```wget ftp://dtn.sdmz.rnp.br/1G_file -O /dados/area-teste/1G_file```

### Axel
```axel ftp://dtn.sdmz.rnp.br/1G_file -o /dados/area-teste/1G_file -n 1```

### aria2c
```aria2c -x1 ftp://dtn.sdmz.rnp.br/1G_file -d /dados/area-teste/1G_file```


## Copiar do DTN ON para DTN USP

### SCP

```scp sdmz@dtn.sciencedmz.on.br:/dados/area-teste/1G_file /dados/area-teste/1G_file```

### GridFTP

* Servidor: 
```globus-gridftp-server -aa &```

* Cliente:

```globus-url-copy -vb -p 1 ftp://dtn.sciencedmz.on.br:2811/dados/area-teste/1G_file file:///dados/area-teste/1G_file```

### Iperf3

* Servidor
```iperf3 -s &```

* Cliente
```perf3 -c dtn.sciencedmz.on.br -P 1 -i1 -O 5 -n 1G```

### UDR
```udr rsync -av -stats --progress sdmz@dtn.sciencedmz.on.br:/dados/area-teste/1G_file /dados/area-teste/1G_file```

### Wget
```wget ftp://dtn.sciencedmz.on.br/1G_file -O /dados/area-teste/1G_file```

### Axel
```axel ftp://dtn.sciencedmz.on.br/1G_file -o /dados/area-teste/1G_file -n 1```

### aria2c
```aria2c -x1 ftp://dtn.sciencedmz.on.br/1G_file -d /dados/area-teste/1G_file```