import requests


class BaseRequest:
    def __init__(self):
        self.headers = {}
        self.auth = None

    def _build_url(self, route):
        raise NotImplementedError

    @staticmethod
    def _handle_response(resp, full_resp=False):
        if resp.status_code in [200, 201]:
            if full_resp:
                return resp
            return resp.json()
        if resp.status_code == 204:
            return True
        print(resp.text, resp.status_code)
        return None

    def request(self, url, method="GET", full_resp=False, **kwargs):
        kwargs = {
            "headers": self.headers,
            "auth": self.auth,
            **kwargs
        }
        resp = requests.request(method=method, url=url, **kwargs)
        return self._handle_response(resp, full_resp=full_resp)

    def get(self, url, **kwargs):
        return self.request(url=url, **kwargs)

    def post(self, url, **kwargs):
        return self.request(url=url, method="POST", **kwargs)

    def put(self, url, **kwargs):
        return self.request(url=url, method="PUT", **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url=url, method="DELETE", **kwargs)
