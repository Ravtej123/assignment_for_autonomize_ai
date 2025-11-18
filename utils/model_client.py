#  POST to /predict or configurable path

class ModelClient():
    def predict(self, payload):
        return self.post('/predict', json=payload)