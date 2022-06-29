import argparse
import requests
import os
from functools import cmp_to_key
from datetime import datetime


def convert_str_to_datetime(value: str, fmt="%B %Y") -> datetime:
    return datetime.strptime(value, fmt)


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

    def post(self, url, **kwargs):
        return self.request(url=url, method="POST", **kwargs)


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


class UploadAttachmentHandler:
    def __init__(self, confluence_service: ConfluenceService):
        self.confluence_service = confluence_service

    def compare_file(self, file1, file2):
        date1, _ = os.path.splitext(file1)
        date2, _ = os.path.splitext(file2)
        date1_obj = convert_str_to_datetime(date1)
        date2_obj = convert_str_to_datetime(date2)
        if date1_obj > date2_obj:
            return -1
        else:
            return 1

    def get_latest_file(self, dir_path):
        list_files = []
        for item in os.listdir(dir_path):
            file_path = os.path.join(dir_path, item)
            if os.path.isfile(file_path):
                date_str, _ = os.path.splitext(item)
                try:
                    convert_str_to_datetime(date_str)
                except:
                    continue
                list_files.append(item)
        list_files = sorted(list_files, key=cmp_to_key(self.compare_file))
        return list_files[0] if len(list_files) else None

    def upload_attachment(self, page_id: str, file_path: str, file_name: str):
        with open(file_path, "rb") as f:
            result = self.confluence_service.upload_attachment(
                page_id=page_id, attachment_data=f, attachment_name=file_name
            )
            if not result:
                print("Upload attachment failed")
            else:
                print("Upload success")

    def main(self, dir_path, page_id: str):
        latest_file = self.get_latest_file(dir_path=dir_path)
        if not latest_file:
            print("There is no file to upload")
        else:
            print("Latest file is:", latest_file)
            file_path = os.path.join(dir_path, latest_file)
            self.upload_attachment(page_id, file_path=file_path, file_name=latest_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Confluence host. Example: https://confluencedomain.com', required=True)
    parser.add_argument('--token', help='Personal Access Token', required=True)
    parser.add_argument('--page-id', help='The confluence page id you want to upload the attachment to', required=True)
    parser.add_argument('--dir', help='The directory path. Default: /var/lib/jenkins/output', default="/var/lib/jenkins/output")
    args = parser.parse_args()

    dir_path = args.dir
    confluence_host = args.host
    personal_access_token = args.token
    confluence_page_id = args.page_id

    confluence_service = ConfluenceService(host=confluence_host, token=personal_access_token)
    handler = UploadAttachmentHandler(confluence_service=confluence_service)
    handler.main(dir_path=dir_path, page_id=confluence_page_id)
