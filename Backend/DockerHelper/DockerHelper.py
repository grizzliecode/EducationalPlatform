import docker
import docker.errors 
from typing import List
import io
import tarfile

class DockerHelperException(Exception):
    pass


class DockerHelper:
    def __init__(self):
        self.client = docker.from_env()

    def __del__(self):
        self.client.close()

    def createContainer(self, containerImage : str, command, volume) -> str:
        try:
            container = self.client.containers.run(image=containerImage, command=command, detach = True)
            return container.id
        except (docker.errors.APIError,docker.errors.ContainerError, docker.errors.ImageNotFound):
            raise DockerHelperException("Image provided was not found or there was an error communicating with the docker daemon.") 
    
    def stopContainer(self, containerId, force:bool):
        try:
            container = self.client.containers.get(container_id=containerId)
            if force == False:
                container.remove()
            else:
                container.remove(force = force)
        except (docker.errors.APIError,docker.errors.NotFound):
            raise DockerHelperException("Container with the id provided was not found or there was an error communicating with the docker daemon.")
    
    def execCommand(self,containerId, command: List[str]):
        try:
            container = self.client.containers.get(container_id=containerId)
            exit_code, output =container.exec_run(cmd=command, stderr=False,stdout=True, detach=True)
            print(output)
            return exit_code
        except (docker.errors.APIError,docker.errors.NotFound) as e:
            raise DockerHelperException(f"Container with the id provided was not found or there was an error communicating with the docker daemon.{e}" )
    
    def coppyToContainer(self,containerId, data_string, container_path, file_name):
        try:
            container = self.client.containers.get(container_id=containerId)

            tar_stream = io.BytesIO()
            with tarfile.open(fileobj=tar_stream, mode='w') as tar:
                tarinfo = tarfile.TarInfo(name=file_name)
                tarinfo.size = len(data_string)
                tar.addfile(tarinfo, io.BytesIO(data_string.encode('utf-8')))
            tar_stream.seek(0)
            container.put_archive(container_path, tar_stream)
        except (docker.errors.APIError,docker.errors.NotFound) as e:
            raise DockerHelperException(f"Container with the id provided was not found or there was an error communicating with the docker daemon.{e}" )
        
    def coppyFromContainer(self,containerId, container_path):
        try:
            container = self.client.containers.get(container_id=containerId)
            tar_stream, _ = container.get_archive(container_path)
            tar_data = io.BytesIO()
            for chunk in tar_stream:
                tar_data.write(chunk)
            tar_data.seek(0)

            with tarfile.open(fileobj=tar_data, mode='r') as tar:
                # Extract the file and read its contents
                file_member = tar.next()
                if file_member:
                    file_content = tar.extractfile(file_member).read().decode('utf-8')
                    return file_content
                else:
                    raise DockerHelperException(f"No file found at {container_path} in container {containerId}")
        except (docker.errors.APIError,docker.errors.NotFound) as e:
            raise DockerHelperException(f"Container with the id provided was not found or there was an error communicating with the docker daemon.{e}" )