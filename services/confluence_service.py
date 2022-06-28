from requests.auth import HTTPBasicAuth
from services.base import BaseRequest


class ConfluenceService(BaseRequest):
    def __init__(self, host, token):
        super().__init__()
        self.host = host
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    def _build_url(self, route):
        return f"{self.host}/rest/api/{route}"

    def upload_attachment(self, page_id, attachment_name, attachment_data):
        url = self._build_url(f"content/{page_id}/child/attachment")
        files = [
            ('file', (attachment_name, attachment_data, 'application/octet-stream'))
        ]
        self.headers["X-Atlassian-Token"] = "nocheck"
        params = {
            "allowDuplicated": True
        }
        data = {
            "minorEdit": True
        }

        reps = self.post(url, files=files, data=data, params=params)
        return reps
