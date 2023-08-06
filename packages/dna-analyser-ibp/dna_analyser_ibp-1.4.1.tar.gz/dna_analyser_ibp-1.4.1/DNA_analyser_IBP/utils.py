# utils.py
# !/usr/bin/env python3
"""
Module with support functions used in multiple files.
"""

import pandas as pd
import re
from requests import Response


def generate_dataframe(res: dict or list) -> pd.DataFrame:
    """
    Generate dataframe from given dict or list.
    :param res: response dict or list from request
    :return: pandas dataframe
    """
    if isinstance(res, list):
        data = pd.DataFrame().from_records(res, columns=res[0].keys())
        return data
    data = pd.DataFrame(data=[res], columns=list(res.keys()))
    return data


def validate_email(value: str) -> bool:
    """
    Validate email for user account
    :param value: email account string
    :return: boolean TRUE if valid email format
    """

    return bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value))


def validate_key_response(
    response: Response, status_code: int, payload_key: str = None
) -> dict:
    """
    Validate and convert json response to dictionary object.
    :param response: Response object from requests
    :param status_code: expected HTTP status code
    :param payload_key: json key for retrieving data
    :return: dictionary data from json
    """

    if response.status_code == status_code:
        data = response.json()
        if payload_key and data and data[payload_key]:  # check if json and key exist
            return data[payload_key]
        elif data:
            return data
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")


def validate_text_response(response: Response, status_code: int) -> str:
    """
    Validate and return text [string] data.
    :param response: Response object from requests
    :param status_code: expected HTTP status code
    :return: string text data
    """
    if response.status_code == status_code:
        if response.text:
            return response.text
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")
