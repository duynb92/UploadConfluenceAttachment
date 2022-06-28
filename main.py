import argparse

from handlers.upload_attachment_handler import UploadAttachmentHandler
from services.confluence_service import ConfluenceService


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
