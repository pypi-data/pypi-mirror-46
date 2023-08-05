import requests
import json
from time import sleep


class Client():
    _url = 'https://api.mltrons.com'
    _upload = '/apis/testing/upload/?type=json'

    def __init__(self, key, id, model):
        self._key = key
        self._id = id
        self._model = model
        self._progress = '/apis/project/'+id+'/task/'
        self._testing = '/apis/deploy/'+model+'/testing/?project='+id
        self._graph = '/apis/deploy/'+id+'/graph/'

    def get_header(self):
        return {
            "Authorization": "Bearer "+ self._key,
            "Content-Type": "application/json"
        }

    def _post_api(self, path, data):
        r = requests.post(
            url=self._url + path,
            headers=self.get_header(),
            data=json.dumps(data)
        )
        return r

    def _get_api(self, path):
        r = requests.get(
            url=self._url + path,
            headers=self.get_header(),
        )
        return r

    def _get_progress(self):
        request = self._get_api(self._progress)
        return json.loads(request.text)

    def upload(self, resource_id, data):
        req_data = {
            'data': resource_id,
            'project': self._id,
            'json': data
        }
        request = self._post_api(self._upload, req_data)

        if request.status_code == 200:
            while True:
                response = self._get_progress()
                try:
                    if response['data']['result']['step'] == 4:
                        break
                    else:
                        sleep(10)
                except:
                    sleep(10)
            return
        else:
            raise Exception('Upload failed!')

    def _get_testing_result(self):
        request = self._get_api(self._graph)
        result = json.loads(request.text)
        return result['data'][0]['data']

    def test(self):
        request = self._get_api(self._testing)
        if request.status_code == 200:
            while True:
                response = self._get_progress()
                try:
                    if response['data']['result']['step'] == 4:
                        break
                    else:
                        sleep(10)
                except:
                    sleep(10)
            return self._get_testing_result()
        else:
            raise Exception('Testing failed!')
