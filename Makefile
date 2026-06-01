# PowerScale CTO JSON Generator - Makefile
# Provides simple commands for Linux/Ubuntu users

.PHONY: help install run clean test verify

help:
	@echo "PowerScale CTO JSON Generator - Available Commands:"
	@echo ""
	@echo "  make install    - Install system dependencies and Python packages"
	@echo "  make run        - Start the application"
	@echo "  make clean      - Remove virtual environment and cached files"
	@echo "  make test       - Run basic tests"
	@echo "  make verify     - Verify bundled PSI configuration files"
	@echo "  make help       - Show this help message"
	@echo ""

install:
	@echo "Installing PowerScale CTO JSON Generator..."
	@chmod +x install.sh
	@./install.sh

run:
	@./run.sh

clean:
	@echo "Cleaning up..."
	@rm -rf venv
	@rm -rf __pycache__
	@rm -rf .pytest_cache
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@echo "Cleanup complete"

test:
	@echo "Running tests..."
	@python3 -c "from app import app; print('✓ Flask app loads successfully')"
	@python3 -c "from app import generate_cto_json, SSD_PSI_CODES; print('✓ PSI codes loaded:', len(SSD_PSI_CODES), 'SSD options')"
	@python3 -c "from psi_database import psi_db, PSI_DATABASE; print('✓ PSI database loaded:', len(PSI_DATABASE), 'categories')"
	@echo "All tests passed"

verify:
	@echo "Verifying bundled PSI configuration files..."
	@echo "Compute configs: $$(ls psi_configs/infinity/compute/*.conf 2>/dev/null | wc -l) files"
	@echo "SSD configs: $$(ls psi_configs/infinity/ssd/*.conf 2>/dev/null | wc -l) files"
	@echo "NIC configs: $$(ls psi_configs/FE/*.conf 2>/dev/null | wc -l) files"
	@echo "Verification complete"
