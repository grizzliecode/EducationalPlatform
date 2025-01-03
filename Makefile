# Makefile for setting up Python virtual environment, installing requirements, and running tests
.PHONY: clean help test install build-wheel

# Variables
VENV_DIR = venv
PYTHON = python3
REQUIREMENTS = requirements.txt
DIST_DIR = DockerHelperPackage/dist
PACKAGE_DIR = DockerHelperPackage  # Replace this with your package name

# Create the virtual environment
$(VENV_DIR)/bin/activate: 
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)."
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)
	@echo "Requirements installed."

# Install requirements
install: install-wheel
	make -C Evaluator


# Build the Python wheel
build-wheel: $(VENV_DIR)/bin/activate
	cd DockerHelperPackage && ../$(VENV_DIR)/bin/python setup.py bdist_wheel 
	cd ..
	@echo "Wheel built and available in $(DIST_DIR)/."

# Copy and install the wheel in the virtual environment
install-wheel: build-wheel
	@echo "Installing the built wheel into the virtual environment..."
	$(VENV_DIR)/bin/pip install $(DIST_DIR)/*.whl
	@echo "Wheel installed in the virtual environment."

# Run tests using the virtual environment's Python interpreter
test: $(VENV_DIR)/bin/activate
	@echo "Running tests using the virtual environment..."
#	find tests -type f -name "*.py" -exec $(VENV_DIR)/bin/python {} +
	$(VENV_DIR)/bin/python -m unittest discover -s tests -p "*.py"
	@echo "All tests completed."

# Clean up virtual environment and build artifacts
clean:
	rm -rf $(VENV_DIR)
	@echo "Virtual environment removed."
	rm -rf DockerHelperPackage/dist
	rm -rf DockerHelperPackage/build
	rm -rf DockerHelperPackage/DockerHelperPackage.egg-info
	@echo "Build artifacts removed."
	find . -type d -name "__pycache__" -exec rm -rf {} + 

# Usage help
help:
	@echo "Available commands:"
	@echo "  make install       - Create virtual environment and install requirements"
	@echo "  make build-wheel   - Build a Python wheel from the package"
	@echo "  make test          - Run the tests for the app using the virtual environment"
	@echo "  make clean         - Remove the virtual environment and clean build artifacts"
