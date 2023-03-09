import json
import logging
from threading import Thread
from urllib.request import Request, urlopen

from pynodinite.core import NodiniteBaseLogEventHandler


class NodiniteLogAPIEventHandler(NodiniteBaseLogEventHandler):
    """A Nodinite Logger which sends data directly to the Log API, circumventing the Pickup Service.

    .. note::

        This is NOT the recommended way of logging to Nodinite, due to the potential lacking
        error handling of messages that had sending failures.

    Log calls can be expanded with event direction, context and/or body by sending these as arguments
    to the logging call:

    log.info("My log message", EventDirections.INTERNAL_INCOMING, {"CorrelationId": "abc123"}, {"Body":"Included"})

    """

    def __init__(
        self,
        logapi_url,
        log_agent_id,
        endpoint_name,
        endpoint_uri,
        endpoint_type_id,
        level=logging.NOTSET,
    ):
        super(NodiniteLogAPIEventHandler, self).__init__(
            log_agent_id, endpoint_name, endpoint_uri, endpoint_type_id, level=level
        )
        self._logapi_url = logapi_url

    def _send_to_log_api(self, record: logging.LogRecord) -> None:
        """Perform the actual sending to the Nodinite Log API

        # Response:
        # {
        #   'ErrorMessage': None,
        #   'EventId': '66a81d2c-9dd2-ec11-9627-00224881007a',
        #   'Status': 0
        # }

        :param record: The log record to send.
        :return: Nothing
        """
        doc = self.format(record)
        req = Request(
            f"{self._logapi_url}/LogAPI/api/logevent",
            json.dumps(doc, ensure_ascii=True).encode("ascii"),
            {"Content-Type": "application/json"},
        )

        with urlopen(req) as response:
            result = json.loads(response.read())

        if result["status"] != 0:
            # Error has occurred.
            # TODO: Handle exceptions?
            pass

    def emit(self, record: logging.LogRecord) -> None:
        Thread(target=self._send_to_log_api, args=(record,)).start()
