#!/bin/bash

tools="aria2c wget axel globus-url-copy iperf scp xrootd fdt.jar"

for tool in $tools; do
        OUTPUT="$(command -v $tool)"
        if [[ "${OUTPUT}" ]]; then
                echo ${OUTPUT}
        else
                # Caso a ferramenta não esteja no /usr/bin esse comando pode ajudar
                whereis $tool
        fi
done
