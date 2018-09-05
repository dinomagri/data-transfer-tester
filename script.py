#/usr/local/bin/python

from whichcraft import which


path_tools = {}
tools = ['aria2c', 'wget', 'axel', 'globus-url-copy',  'iperf', 'scp', 'udt', 'xrootd','fdt.jar']
for tool in tools:
         path_tools[tool] = which(tool)

print path_tools
