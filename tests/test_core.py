import logging

import pytest

from pynodinite import EndpointType
from pynodinite.core import NodiniteBaseLogEventHandler


def test_creation_of_base_handler():
    """Test creation of base class and that logging with it raises an error"""
    handler = NodiniteBaseLogEventHandler(1, "My Endpoint", "C:\\Files", EndpointType.FILE, logging.INFO)
    logger = logging.getLogger("pynodinite-test")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    with pytest.raises(NotImplementedError):
        logger.info("Hello!")
