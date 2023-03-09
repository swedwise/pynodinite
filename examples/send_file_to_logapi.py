"""
Module: send_file_to_logapi.py
This module provides a function to send logs to Nodinite Log API.
"""

from typing import IO
import json
from urllib.request import Request, urlopen


def send_to_log_api(log_api_url: str, f: IO[bytes]) -> dict:
    """Sends logs to the Nodinite Log API endpoint.

     Response:
    {
       'ErrorMessage': None,
       'EventId': '66a81d2c-9dd2-ec11-9627-00224881007a',
       'Status': 0
    }

    Args:
        - logapi_url (str): URL of the Nodinite Log API endpoint
        - f (IO[bytes]): IO stream containing the log data to be sent

    Returns:
        - None

    Raises:
        - N/A

    Example:
        send_to_log_api('https://example.com/Nodinite/Test', io.BytesIO(b'{ "log": "example" }'))
        # Sends a log with content "{ "log": "example" }" to the endpoint
        # 'https://example.com/Nodinite/Test/LogAPI/api/logevent'.

    """

    req = Request(
        f"{log_api_url}/LogAPI/api/logevent",
        f.read(),
        {"Content-Type": "application/json"},
    )
    with urlopen(req) as response:
        result = json.loads(response.read())

    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Send a JSON document to a Nodinite Log API")
    parser.add_argument("logapi_url", help="URL of the Nodinite Log API endpoint")
    parser.add_argument(
        "json_doc_path",
        type=argparse.FileType("rb"),
        help="Path to the JSON document containing the log data",
    )
    args = parser.parse_args()
    results = send_to_log_api(args.logapi_url, args.json_doc_path)
    print(results)


if __name__ == "__main__":
    main()
