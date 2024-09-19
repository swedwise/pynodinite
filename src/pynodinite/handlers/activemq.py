import logging
import threading

try:
    import stomp
except ImportError:
    pass

from pynodinite.core import NodiniteBaseLogEventHandler


class NodiniteActiveMQHandler(NodiniteBaseLogEventHandler):
    def __init__(self, host, port, username, password, destination, log_agent_id, endpoint_name, endpoint_uri, endpoint_type_id):
        super().__init__(log_agent_id, endpoint_name, endpoint_uri, endpoint_type_id)
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.destination = destination

        self.lock = threading.Lock()
        self.conn = None

    def emit(self, record: logging.LogRecord) -> None:
        doc = self.format(record)

        with self.lock:
            if self.conn is None or not self.conn.is_connected():
                self.conn = stomp.Connection([(self.host, self.port)])
                self.conn.set_listener('', stomp.ConnectionListener())
                self.conn.set_socket_keepalive(True, 60)  # set keepalive timeout to 60 seconds
                self.conn.start()
                self.conn.connect(self.username, self.password)

            self.conn.send(body=doc, destination=self.destination)

