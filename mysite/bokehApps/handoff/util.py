import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('portal.ufg.fibre.org.br', port=6622, username='victor@ufg', password='familia061293')

#stdin, stdout, stderr = ssh.exec_command("ls")
#out = stdout.readlines()
#ssh.exec_command("omf exec experiments/" + exp)

stdin, stdout, stderr = ssh.exec_command("ping 8.8.8.8")

for row in iter(stdout.readline, b''):
    string = row.rstrip()
    print string