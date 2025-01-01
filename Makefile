# Makefile for setting up Python virtual environment and installing requirements

# Variables
VENV_DIR = venv
PYTHON = python3
REQUIREMENTS = requirements.txt

# Create the virtual environment
$(VENV_DIR)/bin/activate: 
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)."

# Install requirements
install: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)
	@echo "Requirements installed."

# Clean up virtual environment
clean:
	rm -rf $(VENV_DIR)
	@echo "Virtual environment removed."

# Usage help
help:
	@echo "Available commands:"
	@echo "  make install  - Create virtual environment and install requirements"
	@echo "  make clean    - Remove the virtual environment"
