from unittest import TestCase, main
from DockerHelper import DockerHelper, DockerHelperException
import time

IMAGE = "test-image"
CMD = ["tail", "-f", "/dev/null"]
dh = DockerHelper()

class TestDockerHelper(TestCase):
    def test_create_and_stop(self):
        original_num = len(dh.client.containers.list())
        containerID = dh.createContainer(containerImage=IMAGE, command=CMD, volume=None)
        self.assertIsNotNone(containerID)
        self.assertIsInstance(containerID, str)
        self.assertEqual(original_num+1, len(dh.client.containers.list()))
        dh.stopContainer(containerID, True)
        time.sleep(0.5)
        self.assertEqual(original_num, len(dh.client.containers.list()))
    
    def test_coppy(self):
        original_num = len(dh.client.containers.list())
        message = "Merge baiete dai bataie"
        containerID = dh.createContainer(containerImage=IMAGE, command=CMD, volume=None)
        self.assertIsNotNone(containerID)
        self.assertIsInstance(containerID, str)
        self.assertEqual(original_num+1, len(dh.client.containers.list()))
        dh.coppyToContainer(containerId=containerID, data_string=message, container_path="/work",file_name="testfile.txt")
        time.sleep(0.2)
        new_message = dh.coppyFromContainer(containerId=containerID, container_path="/work/testfile.txt")
        self.assertTrue(message == new_message)
        dh.stopContainer(containerID, True)
        time.sleep(0.5)
        self.assertEqual(original_num, len(dh.client.containers.list()))
        
    def test_exec(self):
        original_num = len(dh.client.containers.list())
        message = "Merge baiete dai bataie"
        containerID = dh.createContainer(containerImage=IMAGE, command=CMD, volume=None)
        self.assertIsNotNone(containerID)
        self.assertIsInstance(containerID, str)
        self.assertEqual(original_num+1, len(dh.client.containers.list()))
        dh.execCommand(containerId=containerID, command = ["/bin/sh", "-c",f"echo {message} > /work/testfile.txt"])
        time.sleep(0.2)
        new_message = dh.coppyFromContainer(containerId=containerID, container_path="/work/testfile.txt")
        dh.stopContainer(containerID, True)
        self.assertTrue(message+chr(10) == new_message)
        time.sleep(0.5)
        self.assertEqual(original_num, len(dh.client.containers.list()))

if __name__ == "__main__":
    main()