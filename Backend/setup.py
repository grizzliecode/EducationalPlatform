from setuptools import setup, find_packages

setup(
    name="DockerHelperPackage",          # Replace with your package name
    version="0.1.0",                     # Replace with your version
    description="A helper package for Docker operations",
    author="Your Name",
    author_email="your_email@example.com",
    packages=find_packages(),            # Automatically detects DockerHelper
    install_requires=[
        # Add dependencies here, if any
    ],
)
