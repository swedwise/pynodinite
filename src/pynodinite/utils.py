import json
import re
from urllib.parse import urljoin
from urllib.request import urlopen


def event_direction_enum_from_logapi(nodinite_log_api_url):
    with urlopen(
        urljoin(nodinite_log_api_url, "/LogAPI/api/logevent/eventdirection"),
    ) as response:
        result = json.loads(response.read())

    print("class EventDirections(Enum):")
    for d in result:
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", d["EnumName"]).upper()
        value = d["EventDirection"]
        print(f"    {name}={value}")


def event_endpoint_id_from_logapi(nodinite_log_api_url):
    with urlopen(
        urljoin(nodinite_log_api_url, "/LogAPI/api/logevent/endpointtypes"),
    ) as response:
        result = json.loads(response.read())

    print("class EndpointType(Enum):")
    for d in result:
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", d["EnumName"]).upper()
        value = d["EndPointTypeId"]
        print(f"    {name}={value}")
