import paramiko
import time

ip_address = '10.25.0.126'
username = 'python'
password = 'SnakeIsALie'

# Enable Debug
# paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

ssh_client = paramiko.SSHClient()
# ssh_client.get_host_keys().clear()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Added the 'look_for_keys=False' flag, and was able to connect.
ssh_client.connect(hostname=ip_address,username=username, password=password, look_for_keys=False)

print("Success login to {}".format(ip_address))
conn = ssh_client.invoke_shell()

conn.send("conf t\n")
conn.send("int lo0\n")
conn.send("ip add 10.1.1.1 255.255.255.255\n")
time.sleep(1)

output = conn.recv(65535)
print(output.decode())

ssh_client.close()