import json

from .base import ReboticsBaseProvider, remote_service


class ODProvider(ReboticsBaseProvider):
    timeout = 60
    retries = 2
    
    @remote_service('/', json=False)
    def ping(self):
        return self.session.get()

    @remote_service('/detect/')
    def detect(self, image, threshold, categories, model_pb_path):
        return self.session.post(data={
            'model_pb_path': model_pb_path,
            'categories': json.dumps(categories),
            'threshold': str(threshold),
        })
