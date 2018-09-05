#/usr/local/bin/python

from whichcraft import which


path_tools = {}
tools = ['aria2c', 'wget', 'axel', 'globus-url-copy', 'iperf', 'scp', 'udt']
for tool in tools:
         path_tools[tool] = which(tool)

print path_tools
