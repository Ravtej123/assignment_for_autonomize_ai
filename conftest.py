import pytest, json, os
import logging
from utils.model_client import ModelClient
from utils.config_reader import Config

# Setup automatic logging
logging.basicConfig(level=logging.INFO, filename='logs\\test_log.log', filemode='w', 
                    format = '%(asctime)s - %(levelname)s - %(message)s')

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call':
        if rep.failed:
            logging.error(f'Test {item.name} failed.')
        else:
            logging.info(f'Test {item.name} passed.')

# fixture to provide config values
@pytest.fixture
def config():
    return Config()

# loading schemas and test data
@pytest.fixture(scope='session')
def agent_schema():
    with open(os.path.join('configs','agent_schema.json')) as f:
        return json.load(f)

@pytest.fixture(scope='session')
def valid_inputs():
    with open(os.path.join('data','valid_inputs.json')) as f:
        return json.load(f)

@pytest.fixture(scope='session')
def malformed_inputs():
    with open(os.path.join('data','malformed_inputs.json')) as f:
        return json.load(f)

@pytest.fixture
def model_client(config):
    return ModelClient(base_url=config['model_api'], token=config.get('token_valid'))
