import requests

try:
    # Python 3
    print('oli 3')
    from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode
except ImportError:
    # Python 2
    print('oli 2')
    from urlparse import urlparse, parse_qsl, urlunparse
    from urllib import urlencode

class Service():

    def __init__(self, user, password, mode='cert'):
        if mode == 'cert':
            self.base_uri = 'https://cert.netpay.com.mx/gateway-ecommerce'
        else:
            self.base_uri = 'http://209cdac2.ngrok.io'
        payload = self._build_login_request(_user, _pass)
        


    def get_jwt_token():
        payload = self._build_login_request(_user, _pass)
        self.access_token = self._build_http_post_request('/v1/auth/login', 'post', payload)



    def _test(self):
        print(self.access_token);
        return True;

    def _build_login_request(self, user, _pass):
        payload = {"security" : {"userName": user,"password": _pass}}
        return payload
        
    def _build_http_get_request(self, end_point, method, **kwargs):

        req = None

        if method == 'get':
            url = "{base_uri}/{end_point}".format(
                base_uri=self.base_uri,
                end_point=end_point
            )

            url = self._update_url_params(url, kwargs)

            req = requests.get(
                url,
                headers=self._set_headers()
            )
        return req

    def _build_http_post_request(self, end_point, method, payload):
        
        req = None
        print(self.base_uri);
        print(end_point);
        if method == 'post':
            url = "{base_uri}/{end_point}".format(
                base_uri=self.base_uri,
                end_point=end_point
            )

            req = requests.request(
                "POST",
                url,
                headers=self._set_not_auth_headers(),
                data=payload,
            )
        return req

    def _set_not_auth_headers(self):

        headers = {
            'Content-Type': "application/json"
        }

        return headers

    def _set_auth_headers(self):

        headers = {
            'Authorization': "Beaarer {token}".format(token=self.access_token),
            'Content-Type': "application/json"
        }

        return headers

    def _update_url_params(self, url, params):

        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)

        return urlunparse(url_parts)

