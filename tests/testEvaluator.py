from unittest import TestCase, main
import subprocess
import time
from DockerHelper import DockerHelper, DockerHelperException

input_file = "./tests/resources/input.txt"
output_file = "./tests/resources/output.txt"
c_source = "./tests/resources/test.cpp"
java_source = "./tests/resources/test.java"
python_source = "./tests/resources/test.py"
wrong_c = "./tests/resources/wrong.cpp"
result = "./tests/resources/result.txt"
clues = "./tests/resources/clues.txt"

IMAGE = "eval-image"
dh = DockerHelper()

class TestEvaluator(TestCase):
    def testCPP(self):
        CMD = ["python", "evaluate.py", "-l", "c/c++", "-i", "input.txt", "-o", "output.txt", "-f","result.txt", "-s", "test.cpp"]
        original_num = len(dh.client.containers.list())
        containerID = dh.createContainer(containerImage=IMAGE, command=["tail", "-f", "/dev/null"], volume=None)
        self.assertIsNotNone(containerID)
        self.assertIsInstance(containerID, str)
        self.assertEqual(original_num+1, len(dh.client.containers.list()))
        with open(input_file) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="input.txt")
        with open(output_file) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="output.txt")
        with open(c_source) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="test.cpp") 
        dh.execCommand(containerId=containerID, command=CMD)
        time.sleep(2)
        output = dh.coppyFromContainer(containerId=containerID,container_path="/work/clues.txt")  
        self.assertEqual("Accepted", output)
        dh.stopContainer(containerID, True)
        time.sleep(0.5)
        self.assertEqual(original_num, len(dh.client.containers.list()))

    def testCPPWromg(self):
        CMD = ["python", "evaluate.py", "-l", "c/c++", "-i", "input.txt", "-o", "output.txt", "-f","result.txt", "-s", "test.cpp"]
        original_num = len(dh.client.containers.list())
        containerID = dh.createContainer(containerImage=IMAGE, command=["tail", "-f", "/dev/null"], volume=None)
        self.assertIsNotNone(containerID)
        self.assertIsInstance(containerID, str)
        self.assertEqual(original_num+1, len(dh.client.containers.list()))
        with open(input_file) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="input.txt")
        with open(output_file) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="output.txt")
        with open(wrong_c) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="test.cpp") 
        dh.execCommand(containerId=containerID, command=CMD)
        time.sleep(2)
        output = dh.coppyFromContainer(containerId=containerID,container_path="/work/clues.txt")  
        self.assertTrue("Runtime exception." in output)
        dh.stopContainer(containerID, True)
        time.sleep(0.5)
        self.assertEqual(original_num, len(dh.client.containers.list()))

    def testJava(self):
        CMD = ["python", "evaluate.py", "-l", "java", "-i", "input.txt", "-o", "output.txt", "-f","result.txt", "-s", "CumulativeSum.java"]
        original_num = len(dh.client.containers.list())
        containerID = dh.createContainer(containerImage=IMAGE, command=["tail", "-f", "/dev/null"], volume=None)
        self.assertIsNotNone(containerID)
        self.assertIsInstance(containerID, str)
        self.assertEqual(original_num+1, len(dh.client.containers.list()))
        with open(input_file) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="input.txt")
        with open(output_file) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="output.txt")
        with open(java_source) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="CumulativeSum.java") 
        dh.execCommand(containerId=containerID, command=CMD)
        time.sleep(2)
        output = dh.coppyFromContainer(containerId=containerID,container_path="/work/clues.txt")  
        self.assertEqual("Accepted", output)
        dh.stopContainer(containerID, True)
        time.sleep(0.5)
        self.assertEqual(original_num, len(dh.client.containers.list()))

    def testPython(self):
        CMD = ["python", "evaluate.py", "-l", "python", "-i", "input.txt", "-o", "output.txt", "-f","result.txt", "-s", "test.py"]
        original_num = len(dh.client.containers.list())
        containerID = dh.createContainer(containerImage=IMAGE, command=["tail", "-f", "/dev/null"], volume=None)
        self.assertIsNotNone(containerID)
        self.assertIsInstance(containerID, str)
        self.assertEqual(original_num+1, len(dh.client.containers.list()))
        with open(input_file) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="input.txt")
        with open(output_file) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="output.txt")
        with open(python_source) as fin:
            dh.coppyToContainer(containerId=containerID,data_string=fin.read(),container_path="/work", file_name="test.py") 
        dh.execCommand(containerId=containerID, command=CMD)
        time.sleep(2)
        output = dh.coppyFromContainer(containerId=containerID,container_path="/work/clues.txt")  
        self.assertEqual("Accepted", output)
        dh.stopContainer(containerID, True)
        time.sleep(0.5)
        self.assertEqual(original_num, len(dh.client.containers.list()))    

if __name__ == "__main__":
    main()

