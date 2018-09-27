import subprocess
import sys

HOST="dtn.sciencedmz.usp.br"
# Ports are handled in ~/.ssh/config since we use OpenSSH
COMMAND="bash /tmp/check_tools.sh"

ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
if result == []:
    error = ssh.stderr.readlines()
    print >>sys.stderr, "ERROR: %s" % error
else:
    print(result)
    final = [x[:-1] for x in result]
    print(final)