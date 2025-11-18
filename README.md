# Agent & Model Integration Pytest Framework

This repository contains a pytest-based automation framework for testing:
- Agent Integration (data extraction, schema validation, authentication, resilience)
- Model Integration (prediction correctness, malformed input handling, bias, performance)

Structure:
- tests/: pytest test files for agent and model integration
- utils/: helper scripts
- configs/: schema and config files
- data/: sample test payloads
- reports/: test run outputs (Allure)

How to run:
1. Create a virtualenv and install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Adjust `configs/config.ini` to point to your test endpoints.
3. Run tests:
   ```bash
   pytest
   ```
4. View Allure report:
   ```bash
   allure serve reports
   ```