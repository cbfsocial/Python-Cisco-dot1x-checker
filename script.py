import paramiko
import os

usr = "username"
pwd = "password"

hosts = []


def list_to_str(device_output):
    emp = ''
    done = emp.join(device_output)
    return done


def hostname_parser(host):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=usr, password=pwd, look_for_keys=False, allow_agent=False)
    stdin, stdout, stderr = client.exec_command('sh run | i hostname')
    return stdout.readlines()[0].replace('hostname ', '').replace('\r\n', '')


def port_parser(host, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=usr, password=pwd, look_for_keys=False, allow_agent=False)
    stdin, stdout, stderr = client.exec_command("show run int GigabitEthernet1/0/" + str(port))
    lines = stdout.readlines()
    return lines


for host in hosts:
    hst = hostname_parser(host)
    f = open("dot1x_rev2.txt", 'a')
    f.write('\r\n' + '------------- ' + hst + ' ------------- ' + '\r\n')
    print(host)
    for port in range(1, 49):
        info = port_parser(host, port)
        total = list_to_str(info)
        total = list(filter(None, total))
        total = list_to_str(total)
        if 'switchport' in total:
            if 'authentication' in total:
                if 'port-control' not in total:
                    f.write("GigabitEthernet1/0/" + str(port) + ' has force-authorized \r\n')
                else:
                    f.write("GigabitEthernet1/0/" + str(port) + ' has dot1x ON \r\n')
            else:
                f.write("GigabitEthernet1/0/" + str(port) + ' has dot1x OFF \r\n')
f.close()
