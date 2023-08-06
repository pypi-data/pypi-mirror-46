import logging
import requests
from typing import Dict

from confluence.exceptions.generalerror import ConfluenceError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ConfluenceResourceNotFound(ConfluenceError):
    """Corresponds to 404 errors on the REST API."""

    def __init__(self, path, params, response):
        # type: (str, Dict[str, str], requests.Response) -> None
        msg = 'Resource was not found at path {} or the user has insufficient permissions'.format(path)
        super(ConfluenceResourceNotFound, self).__init__(path, params, response, msg)
