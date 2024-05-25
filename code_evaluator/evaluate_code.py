import docker

def evaluate_code(code, command, script):
    client = docker.from_env()
    
    # Create a volume
    volume = client.volumes.create(name="code_evaluator")
    
    # Create a container with the volume and memory limit
    container = client.containers.run("python:3.8", detach=True, volumes={volume.name: {'bind': '/mnt/volume', 'mode': 'rw'}}, mem_limit="512m")
    
    # Execute the code
    output = container.exec_run(command)
    print(output)
    
    # Stop and remove the container
    container.stop()
    container.remove()
    
    # Remove the volume
    volume.remove()
    
    return True

if __name__ == "__main__":
    evaluate_code("", "ls", "default")