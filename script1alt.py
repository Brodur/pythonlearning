import paramiko

t = paramiko.Transport(('10.25.0.126', 22))
t.connect(username='python', password='SnakeIsALie')
ssh = paramiko.SSHClient()
ssh._transport = t
stdin, stdout, stderr = ssh.exec_command('show version')

print('INPUT')
print(stdin)
print('OUTPUT')
for line in stdout.readlines():
  print(line, end='')

print('ERROR')
print(stderr.readlines())

ssh.close()
t.close()