import paramiko
import time

ip_address = '10.25.0.126'
username = 'python'
password = 'SnakeIsALie'

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_address, username=username, password=password)

print("Successfully connected to {}".format(ip_address))
conn = ssh_client.invoke_shell()

conn.send("configure terminal\n")
conn.send("interface lo0\n")
conn.send("ip add 10.254.254.254 255.255.255.255\n")
time.sleep(1)

output = conn.recv(65535)
print(output.decode())

ssh_client.close()