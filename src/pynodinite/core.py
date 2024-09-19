import base64
import datetime
import getpass
import json
import logging
import os
import platform

from pynodinite.enums import EndpointType, EventDirections




class NodiniteBaseLogEventHandler(logging.Handler):
    def __init__(
        self,
        log_agent_id,
        endpoint_name,
        endpoint_uri,
        endpoint_type_id,
        level=logging.NOTSET,
    ):
        super(NodiniteBaseLogEventHandler, self).__init__(level=level)

        self.log_agent_id = log_agent_id
        self.endpoint_name = endpoint_name
        self.endpoint_uri = endpoint_uri
        self.endpoint_type_id = (
            endpoint_type_id.value if isinstance(endpoint_type_id, EndpointType) else endpoint_type_id
        )

    def format(self, record: logging.LogRecord) -> str:
        """The main formatting method for the Nodinite handlers.

        --- Mandatory ---
        number  LogAgentValueId  - Who (Log Agents) sent the data
        string  EndPointName - Name of Endpoint transport
        string  EndPointUri - URI for Endpoint transport
        number  EndPointDirection - Direction for Endpoint transport
        number  EndPointTypeId - Type of Endpoint transport
        string  OriginalMessageTypeName - Message Type Name
        string  LogDateTime - Client Log datetime (UTC format)
        --- Optional ---
        number  EventDirection - External Incoming (before receive port)
        string  ProcessingUser - Log Identity on format "DOMAIN\\user"
        number  SequenceNo - Provide your own sequence number
        number  EventNumber - Provide your own event number
        string  LogText - Your log text goes here
        string  ApplicationInterchangeId - Id for Application scope
        guid    LocalInterchangeId - Id for local scope
        string  LogStatus - As defined for each Log Agent
        string  ProcessName - Name of process
        string  ProcessingMachineName - Name of server where log event originated
        string  ProcessingModuleName - Name of module
        string  ProcessingModuleType - Type of module, exe, dll, service
        guid    ServiceInstanceActivityId - Id for run scope
        string  ProcessingTime - Flow execution time so far in milliseconds

        """
        dt = datetime.datetime.now()
        # TODO: How to handle context values? Args? Extra?
        direction = record.args[0].value if record.args else EventDirections.DEFAULT.value
        context = record.args[1] if record.args and len(record.args) > 1 and isinstance(record.args[1], dict) else {}
        body = record.args[2] if record.args and len(record.args) > 2 else ""
        if record.exc_text:
            context["Exception"] = record.exc_text
        doc = {
            # Required fields ----------------------------------------------------------
            "LogAgentValueId": self.log_agent_id,  # Who (Log Agents) sent the data
            "EndPointName": self.endpoint_name,  # Name of Endpoint transport
            "EndPointUri": self.endpoint_uri,  # URI for Endpoint transport
            "EndPointDirection": 1,  # Direction for Endpoint transport
            "EndPointTypeId": self.endpoint_type_id,  # Type of Endpoint transport
            "OriginalMessageTypeName": record.name,  # The name of the message type
            "LogDateTime": dt.isoformat(),  #datetime.datetime.fromtimestamp(record.created).isoformat(),
            # Optional fields ----------------------------------------------------------
            "SequenceNo": record.args[3] if record.args and len(record.args) > 3 else "",
            "EventDirection": direction,
            "ProcessingUser": f"{os.environ['userdomain']}\\{getpass.getuser()}",
            "LogText": record.msg,
            "LogStatus": str(record.levelno),
            "ProcessName": record.processName,
            "ProcessingMachineName": platform.node(),
            "ProcessingModuleName": __name__,
            "ProcessingModuleType": "pyNodinite",
            "Body": base64.b64encode(body.encode()).decode("ascii"),
            "Context": context,
        }
        return json.dumps(doc)

    def emit(self, record: logging.LogRecord) -> None:
        raise NotImplementedError("Do not use this base class!")
