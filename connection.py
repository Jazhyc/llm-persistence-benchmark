import paramiko
import boto3
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
    client.connect(hostname=ip, username="ubuntu", pkey=k, look_for_keys=False)
    return client


def evaluate_code(client, command):
    # Execute a command and capture the output
    stdin, stdout, stderr = client.exec_command(command)

    # Close the connection
    #client.close()

    return stdout.read().decode()
