from unittest import TestCase, main
from DockerHelper import DockerHelper, DockerHelperException

IMAGE = "test-image"
CMD = ["tail", "-f", "/dev/null"]
dh = DockerHelper()

class TestDockerHelper(TestCase):
    def test_create(self):
        containerID = dh.createContainer(containerImage=IMAGE, command=CMD, volume=None)
        self.assertIsNotNone(containerID)
        self.assertIsInstance(containerID, str)
    


if __name__ == "__main__":
    main()