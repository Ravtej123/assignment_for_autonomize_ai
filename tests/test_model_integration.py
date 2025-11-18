import pytest
import time

# MI-01: Model Output for Valid Structured Input
def test_mi_01(model_client, valid_inputs):
    payload = valid_inputs['model_valid']
    response = model_client.predict(payload)
    assert response.status_code == 200
    assert 'class_label' in response.json()
    assert 'confidence' in response.json() and response.json()['confidence'] >= 0.0

# MI-02: Handling Malformed or Adversarial Inputs
def test_mi_02(model_client, malformed_inputs):
    payload = malformed_inputs['model_malformed']
    response = model_client.predict(payload)
    # Model should not crash; expected statuses: 200 with fallback or 4xx/5xx gracefully
    assert response.status_code in (200,400,422,503)
    if response.status_code == 200:
        assert 'class_label' in response.json() or 'error' in response.json()

# MI-03: Incomplete/Ambiguous Input Behavior
def test_mi_03(model_client):
    payload = {"age":45, "symptoms":["fatigue"]}  # ambiguous
    response = model_client.predict(payload)
    assert response.status_code in (200,400,422)
    if response.status_code == 200:        
        if 'confidence' in response.json():
            assert response.json()['confidence'] < 0.9 
            assert response.json().get('require_human_review', False)

# MI-04: Fairness / Bias Basic Check
@pytest.mark.parametrize('gender', ['male','female','other'])
def test_mi_04(model_client, gender):
    base = {"age":50, "symptoms":["cough","fever"]}
    base['gender'] = gender
    response = model_client.predict(base)
    assert response.status_code == 200
    assert 'class_label' in response.json()

# MI-05: Model Performance - simple concurrency smoke
def test_mi_05(model_client, valid_inputs, config):
    threshold_ms = int(config.get('threshold_ms', 10000))
    payload = valid_inputs['model_valid']
    start = time.time()
    response = model_client.predict(payload)
    duration_ms = (time.time() - start) * 1000
    assert response.status_code == 200
    assert duration_ms < threshold_ms
