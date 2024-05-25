import docker

def evaluate_code(code, command, script):
    client = docker.from_env()
    
    # Create a volume
    volume = client.volumes.create()
    
    code_file_creation_command = f'echo "{code}" > main.txt'
    
    print(code_file_creation_command)
    
    # Add code to the volume
    code_creation = client.containers.run("debian", command=code_file_creation_command, volumes={volume.name: {'bind': '/mnt/volume', 'mode': 'rw'}}, mem_limit="512m", working_dir="/mnt/volume", privileged=True)
    
    print("File: ", code_creation)
    
    output = client.containers.run("debian", command='ls', volumes={volume.name: {'bind': '/mnt/volume', 'mode': 'rw'}}, mem_limit="512m", working_dir="/mnt/volume")
    
    print("Output: ", output)
    
    # Persistance technique
    persistance_success = client.containers.run("debian", command=command, volumes={volume.name: {'bind': '/mnt/volume', 'mode': 'rw'}}, mem_limit="512m", working_dir="/mnt/volume", privileged=True)
    
    print("Persistance: ", persistance_success)
    
    # reboot the container
    client.containers.prune()
    
    # Check if the data was saved
    output = client.containers.run("debian", command='ls', volumes={volume.name: {'bind': '/mnt/volume', 'mode': 'rw'}}, mem_limit="512m", working_dir="/mnt/volume")
    
    print("Output: ", output)
    
    return True

if __name__ == "__main__":
    evaluate_code("", "touch hello.txt", "default")