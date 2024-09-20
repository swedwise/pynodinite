import json
import logging
import pathlib
import uuid
from threading import Thread

from pynodinite.core import NodiniteBaseLogEventHandler


class NodiniteFileLogEventhandler(NodiniteBaseLogEventHandler):
    """A Nodinite Logger emitter which saves JSON files on disk.

    Log calls can be expanded with event direction, context and/or body by sending these as arguments
    to the logging call:

    log.info("My log message", EventDirections.INTERNAL_INCOMING, {"CorrelationId": "abc123"}, {"Body":"Included"})

    """

    def __init__(
        self,
        dir_path,
        log_agent_id,
        endpoint_name,
        endpoint_uri,
        endpoint_type_id,
        level=logging.NOTSET,
    ):
        super(NodiniteFileLogEventhandler, self).__init__(
            log_agent_id, endpoint_name, endpoint_uri, endpoint_type_id, level=level
        )
        self._path = pathlib.Path(dir_path)

    def _save_json_to_file(self, record: logging.LogRecord):
        doc = self.format(record)
        with self._path.joinpath(f"{uuid.uuid4()}.json").open(mode="wt") as f:
            f.write(doc)

    def emit(self, record: logging.LogRecord) -> None:
        # Perform a fire and forget operation on separate thread.
        Thread(target=self._save_json_to_file, args=(record,)).start()
