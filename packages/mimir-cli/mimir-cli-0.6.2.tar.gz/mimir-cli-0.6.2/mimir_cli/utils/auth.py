"""
authentication related helper functions
"""
import json
import os
import requests
from mimir_cli.strings import MIMIR_DIR, MIMIR_CREDS_PATH, ERR_NOT_AUTH
from mimir_cli.utils.io import mkdir
from mimir_cli.utils.state import debug, error_out, api_login_url


def _request(url, method="GET", **kwargs):
    """request helper"""
    credentials = _read_credentials()
    headers = (
        {"Authorization": credentials["api_token"]}
        if "api_token" in credentials
        else {}
    )
    cookies = credentials if "user_session_id" in credentials else {}
    return requests.request(method, url, cookies=cookies, headers=headers, **kwargs)


def post(url, **kwargs):
    """perform a post request to mimir classroom"""
    return _request(url, method="POST", **kwargs)


def get(url, **kwargs):
    """perform a get request to mimir classroom"""
    return _request(url, method="GET", **kwargs)


def login_to_mimir(email, password):
    """logs into the platform api"""
    login_request = requests.post(
        api_login_url(), data={"email": email, "password": password}
    )
    data = json.loads(login_request.text)
    debug(data)
    if data["success"]:
        cookies = login_request.cookies.get_dict()
        _write_credentials(cookies)
    return data["success"]


def logout_of_mimir():
    """logs out of mimir"""
    os.remove(MIMIR_CREDS_PATH)
    return True


def _read_credentials():
    """reads the user credentials from the mimir directory"""
    mkdir(MIMIR_DIR)
    if os.path.isfile(MIMIR_CREDS_PATH):
        with open(MIMIR_CREDS_PATH, "r") as mimir_credentials_file:
            credentials = json.loads(mimir_credentials_file.read())
        if credentials and (
            "user_session_id" in credentials or "api_token" in credentials
        ):
            return credentials
    error_out(ERR_NOT_AUTH)
    return None


def _write_credentials(cookies):
    """writes the user credentials to the mimir directory"""
    mkdir(MIMIR_DIR)
    credentials = json.dumps(cookies)
    with open(MIMIR_CREDS_PATH, "w") as mimir_credentials_file:
        mimir_credentials_file.write(credentials)
