import json
import logging
import uuid
from threading import Thread

from pynodinite.core import NodiniteBaseLogEventHandler
from pynodinite.exceptions import PyNodiniteException

try:
    import win32com.client

    CAN_BE_USED = True
except (ImportError, NameError):
    CAN_BE_USED = False


class NodiniteMSMQHandler(NodiniteBaseLogEventHandler):
    """

    Example ``msmq_adress``: ``"Direct=OS:localhost\\private$\\myQueueName"``

    """

    def __init__(self, msmq_adress, log_agent_id, endpoint_name, endpoint_uri, endpoint_type_id):
        super().__init__(log_agent_id, endpoint_name, endpoint_uri, endpoint_type_id)
        self.msmq_adress = msmq_adress
        if not CAN_BE_USED:
            raise PyNodiniteException("Install pynodinite with [msmq] option to enable use of MSMQ Handler!")

    def emit(self, record: logging.LogRecord) -> None:
        Thread(target=self._send_json_to_msmq, args=(record,)).start()

    def _send_json_to_msmq(self, record):
        doc = self.format(record)
        qinfo = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
        qinfo.FormatName = self.msmq_adress
        queue = qinfo.Open(2, 0)  # Open a ref to queue
        msg = win32com.client.Dispatch("MSMQ.MSMQMessage")
        msg.Label = f"Nodinite Log Event: {uuid.uuid4()}"
        msg.Body = json.dumps(doc, ensure_ascii=True).encode("ascii")
        msg.Send(queue)
        queue.Close()
