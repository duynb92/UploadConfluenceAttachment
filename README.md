## Prerequisites

- Python 3.8 [Installation & Setup Guide](https://realpython.com/installing-python/) (Python Full Installer)

## Installation

- Install Python package

    **Notes:** You should enter root folder before install

    If you have Python full installer, you can be using `pip` :

    ```
    pip install -r requirements.txt
    ```
  
## Run

  ```commandline
  # Show helper
  python main.py -h
  
  # Run
  python main.py --host https://<yourdomain.com> --token <your_personal_access_token> --page-id <page_id> --dir /var/lib/jenkins/output
  ```