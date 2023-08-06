import requests
import json
import netpay_ecommerce

class Client:

    def __init__(self,url,method,data=None,token=None):

        self.url = netpay_ecommerce.BASE_URL + url

        self.method = method.upper()

        self.data = None

        if data:
            self.data = json.dumps(data)

        self.token = None

        if token:
            self.token = token

    def to_json(self):
        return self._execute().json()
    
    def _execute(self):
        headers = {
            "content-type": "application/json"
        }

        if self.token:
            headers["Authorization"] = "Bearer {}".format(self.token)

        response = None
        response = getattr(requests,self.method.lower())(
            url = self.url,
            headers = headers,
            data = self.data,
            timeout = 360
        )
        return response


