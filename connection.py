import paramiko
import boto3
import time
from os.path import dirname, abspath

file_directory = dirname(abspath(__file__))


def ssh_connection(instance_id):
    ec2_client = boto3.client('ec2', region_name='eu-central-1')

    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    reservations = response['Reservations']

    ip = None

    for reservation in reservations:
        for instance in reservation['Instances']:
            ip = instance.get('PublicIpAddress')

    k = paramiko.RSAKey.from_private_key_file(
        file_directory + "/hckthn.pem")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while True:
        try:
            client.connect(hostname=ip, username="ubuntu", pkey=k, look_for_keys=False)
            break
        except:
            print("could not connect, trying again in 10 seconds")
            time.sleep(10)
    client.connect(hostname=ip, username="ubuntu", pkey=k, look_for_keys=False)
    return client


def evaluate_code(client, command):
    # Execute a command and capture the output
    stdin, stdout, stderr = client.exec_command(command)

    # Close the connection
    #client.close()

    # decode and combine stderr and stdout
    combined = stdout.read().decode() + stderr.read().decode()

    return combined

client = ssh_connection("i-00b479c65d35bbaea")
print(evaluate_code(client, 'find . -name "hello.txt" -type f'))