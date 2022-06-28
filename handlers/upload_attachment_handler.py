import os
from functools import cmp_to_key
from services.confluence_service import ConfluenceService
from utils.handle_datetime import convert_str_to_datetime


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

