import logging

from pynodinite.core import NodiniteBaseLogEventHandler


class NodiniteAzureEventHubHandler(NodiniteBaseLogEventHandler):
    def __init__(self, log_agent_id, endpoint_name, endpoint_uri, endpoint_type_id):
        super().__init__(log_agent_id, endpoint_name, endpoint_uri, endpoint_type_id)
        raise NotImplementedError()

    def emit(self, record: logging.LogRecord) -> None:
        pass
