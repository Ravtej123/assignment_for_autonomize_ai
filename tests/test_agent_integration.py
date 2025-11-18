import pytest
import requests
from utils.schema_validator import validate_schema

# AG-01: Successful Data Extraction and Schema Validation
def test_ag_01(agent_schema):
    response = requests.get('/patient/P12345')
    assert response.status_code == 200, f'Unexpected status {response.status_code}'
    data = response.json()
    ok, err = validate_schema(data, agent_schema)
    assert ok, f'Schema validation failed: {err}'

# AG-02: Handling Missing Required Fields
def test_ag_02():
    resp = requests.get('/patient/missing_fields')
    assert resp.status_code in (400,422,200)
    # If 200, expect an error field in payload
    if resp.status_code == 200:
        body = resp.json()
        assert 'error' in body or 'patient_id' not in body

# AG-03: Detect Incorrect Data Types and Formats
def test_ag_03():
    resp = requests.get('/patient/bad_date_format')
    assert resp.status_code in (200,400,422)
    if resp.status_code == 200:
        data = resp.json()
        if 'dob' in data:
            assert data['dob'].count('-') == 2 or 'error' in data

# AG-04: Connectivity Failure Handling (resilience)
def test_ag_04():
    resp = requests.get('/patient/intermittent')
    assert resp.status_code in (200,503,504,502)

# AG-05: Invalid Credentials Handling
def test_ag_05(config):
    invalid_token = config.get('VALUES', 'token_invalid')
    headers = {"Content-Type":"application/json"}
    headers["Authorization"] = f"Bearer {invalid_token}"
    resp = requests.get('/patient/P12345', headers=headers)
    assert resp.status_code in (401,403)
