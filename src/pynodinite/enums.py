from enum import Enum


class EndpointDirection(Enum):
    # Receive - One-Way, for example, receive a file from a folder
    RECEIVE = 0
    # Send -One-Way, for example, send a file to SFTP
    SEND = 1
    # Two-way Receive -For example an An API sponsoring incoming requests
    TWOWAY_RECEIVE = 10
    # Two-way Send - A client calling some REST API or a call to a stored parameterized procedure
    TWOWAY_SEND = 11
    # None - Please avoid this option
    NONE = -2
    # Unknown -	Default if not set/found (Please avoid this option)
    UNKNOWN = -1


class EventDirections(Enum):
    DEFAULT = None
    EXTERNAL_INCOMING = 17
    EXTERNAL_INCOMING_REQUEST = 21
    EXTERNAL_INCOMING_RESPONSE = 25
    EXTERNAL_OUTGOING = 18
    EXTERNAL_OUTGOING_REQUEST = 22
    EXTERNAL_OUTGOING_RESPONSE = 26
    INTERNAL_INCOMING = 33
    INTERNAL_OUTGOING = 34
    PROCESS_INCOMING = 65
    PROCESS_OUTGOING = 66


class EndpointType(Enum):
    UNKNOWN = 0
    BIZTALK_RECEIVE = 1
    BIZTALK_SEND = 2
    BIZTALK_DYNAMIC_SEND = 3
    BIZTALK_LOGICAL_RECEIVE = 4
    BIZTALK_LOGICAL_SEND = 5
    LOG4NET = 9
    MSMQ = 10
    ACTIVEMQ = 11
    RABBITMQ = 12
    AMQP = 13
    ANYPOINT_M_Q = 14
    APP_FABRIC = 20
    MULE = 25
    CLOUD_HUB = 26
    APP_FABRIC_AZURE = 30
    WMQ = 40
    IBM_M_Q = 40
    IBM_INTEGRATION_BUS = 41
    IBM_DATA_QUEUE = 42
    IBM_API_CONNECT = 43
    IBM_DATA_POWER_GATEWAY = 44
    IBM_EVENT_STREAMS = 45
    IBM_WATSON_IO_T_PLATFORM = 46
    IBM_CLOUD_FUNCTIONS = 47
    WCF = 50
    FILE = 60
    DROPBOX = 61
    SMTP = 65
    MICROSOFT_AZURE_SERVICE_BUS = 70
    MICROSOFT_AZURE_API_MANAGEMENT = 71
    MICROSOFT_AZURE_API_APPS = 72
    MICROSOFT_AZURE_LOGIC_APPS = 73
    MICROSOFT_AZURE_LOG_AUDITS = 74
    MICROSOFT_AZURE_FUNCTIONS = 75
    FTP = 80
    FTPS = 81
    SFTP = 82
    CONNECT_DIRECT = 83
    HTTP = 85
    HTTPS = 86
    REST_API = 87
    WEB_API = 88
    ODBC = 90
    JDBC = 91
    SQL = 92
    DATABASE = 93
    SSIS = 94
    AMAZON_DYNAMO_DB = 95
    AMAZON_S3 = 96
    POSTGRESQL = 97
    MLLP = 130
    APACHE_KAFKA = 140
