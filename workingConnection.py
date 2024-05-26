import paramiko


def ssh_connect_and_execute_command(hostname, port, username, key_file_path, command):
    k = paramiko.RSAKey.from_private_key_file(
        "/home/davidez/Nextcloud/THE PROJECTS FOLDER/AISIG/AIEvaluations Hackathon/Hackathon Tinkering EC2 "
        "instance/HackathonTinkering.pem")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='13.49.221.6', username="ubuntu", pkey=k, allow_agent=False, look_for_keys=False)

    # Execute a command and capture the output
    stdin, stdout, stderr = client.exec_command(command)

    # Read the output
    stdout_text = stdout.read().decode()
    stderr_text = stderr.read().decode()

    # Close the connection
    client.close()

    return stdout_text, stderr_text


# Replace these values with your server details and command
hostname = 'ec2-13-49-221-6.eu-north-1.compute.amazonaws.com'
port = 22
username = 'ec2-user'
key_file_path = ('/home/davidez/Nextcloud/THE PROJECTS FOLDER/AISIG/AIEvaluations Hackathon/Hackathon Tinkering EC2 '
                 'instance/public.pub')
command = 'ls -la'

if __name__ == "__main__":

    # Call the function
    stdout, stderr = ssh_connect_and_execute_command(hostname, port, username, key_file_path, command)

    print("Standard Output:")
    print(stdout)
    print("Standard Error:")
    print(stderr)
