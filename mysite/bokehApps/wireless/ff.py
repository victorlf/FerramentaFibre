import subprocess

proc = subprocess.Popen(["iwlist", "dd", "scan"], stdout=subprocess.PIPE, universal_newlines=True)
out, err = proc.communicate()

print "oioioioiooi"