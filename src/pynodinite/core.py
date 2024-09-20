import base64
import datetime
import getpass
import json
import logging
import os
import platform

from pynodinite.enums import EndpointType, EventDirections, EndpointDirection




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
        if hasattr(record, "Nodinite"):
            nodinite = record.Nodinite
        else:
            nodinite = {}

        body = base64.b64encode(nodinite.get("Body", "").encode()).decode("ascii")
        context = nodinite.get("Context", {})
        if record.exc_text:
            context["Exception"] = record.exc_text

        doc = {
            # Required fields ----------------------------------------------------------
            "LogAgentValueId": nodinite.get("LogAgentValueId", self.log_agent_id),  # Who (Log Agents) sent the data
            "EndPointName": nodinite.get("EndPointName", self.endpoint_name),  # Name of Endpoint transport
            "EndPointUri": nodinite.get("EndPointUri", self.endpoint_uri),  # URI for Endpoint transport
            "EndPointDirection": nodinite.get("EndPointDirection", EndpointDirection.SEND).value,  # Direction for Endpoint transport
            "EndPointTypeId": nodinite.get("EndPointTypeId", self.endpoint_type_id),  # Type of Endpoint transport
            "OriginalMessageTypeName": nodinite.get("EndPointTypeId", record.name),  # The name of the message type
            "LogDateTime": datetime.datetime.fromtimestamp(record.created).isoformat(),
            # Optional fields, but with defaults ---------------------------------------
            "EventDirection": nodinite.get("EventDirection", EventDirections.DEFAULT).value,
            "ProcessingUser": f"{os.environ['userdomain']}\\{getpass.getuser()}",
            "ProcessName": nodinite.get("ProcessName", record.processName),
            "ProcessingMachineName": nodinite.get("ProcessingMachineName", platform.node()),
            "ProcessingModuleName": nodinite.get("ProcessingModuleName", __name__),
            "ProcessingModuleType": nodinite.get("ProcessingModuleType", "pyNodinite"),
            # Optional fields ----------------------------------------------------------
            "SequenceNo": nodinite.get("SequenceNo", None),
            "EventNumber": nodinite.get("EventNumber", None),
            "ApplicationInterchangeId": nodinite.get("ApplicationInterchangeId", None),  # str Id for Application scope
            "LocalInterchangeId": nodinite.get("LocalInterchangeId", None),              # guid Id for local scope
            "ServiceInstanceActivityId": nodinite.get("ProcessingModuleType", None),     # guid  Id for run scope
            "ProcessingTime": nodinite.get("ProcessingTime", None), # Flow execution time so far in milliseconds
            # Data fields --------------------------------------------------------------
            "LogText": record.msg,
            "LogStatus": nodinite.get("LogStatus", str(record.levelno)),
            "Body":  body,
            "Context": context,
        }
        return json.dumps(doc)

    def emit(self, record: logging.LogRecord) -> None:
        raise NotImplementedError("Do not use this base class!")
