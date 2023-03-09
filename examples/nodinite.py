import logging

from pynodinite import NodiniteLogAPIEventHandler, NodiniteFileLogEventhandler
from pynodinite.enums import EndpointType, EventDirections


def main():
    logger = logging.getLogger("MyNodiniteEventLogger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(
        NodiniteLogAPIEventHandler(
            "https://nodiniteinstall.westeurope.cloudapp.azure.com/Nodinite/Test",
            2,
            "Python API Handler",
            "http://localhost:8000",
            EndpointType.HTTPS,
            level=logging.INFO,
        )
    )
    file_handler = NodiniteFileLogEventhandler(
        "C:\\Logs\\",
        1,
        "Python Doc Handler",
        "http://localhost:8000",
        EndpointType.HTTPS,
        level=logging.INFO,
    )
    logger.addHandler(file_handler)

    logger.debug("An debug event")
    logger.info(
        "An info event",
        EventDirections.INTERNAL_INCOMING,
        {"CorrelationId": "abc123"},
        {"Body": "Included"},
    )
    logger.warning(
        "A warning event",
        EventDirections.INTERNAL_OUTGOING,
        {"CorrelationId": "abc123"},
        {"Body": "Included"},
    )
    try:
        raise ValueError("Wrong!")
    except Exception:  # noqa
        logger.error(
            "A error event",
            EventDirections.INTERNAL_OUTGOING,
            {"CorrelationId": "abc123"},
            {"Body": "Included"},
            exc_info=True,
        )

    logger.critical(
        "A critical event!",
        EventDirections.INTERNAL_OUTGOING,
        {"CorrelationId": "abc123"},
        {"Body": "Included"},
        exc_info=True,
    )


if __name__ == "__main__":
    main()
