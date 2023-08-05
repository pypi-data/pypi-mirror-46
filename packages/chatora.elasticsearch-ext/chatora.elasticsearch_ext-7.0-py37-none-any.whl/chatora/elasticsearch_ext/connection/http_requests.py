__all__ = (
    'create_requests_http_connection_factory',
)

import typing

from elasticsearch import RequestsHttpConnection
from requests.adapters import (
    DEFAULT_POOLBLOCK,
    DEFAULT_POOLSIZE,
    DEFAULT_RETRIES,
    HTTPAdapter,
)
from urllib3.util.retry import Retry


# https://stackoverflow.com/questions/34837026/whats-the-meaning-of-pool-connections-in-requests-adapters-httpadapter

def create_requests_http_connection_factory(
    connection_factory: typing.Callable = RequestsHttpConnection,
    adapter_pool_connections: int = DEFAULT_POOLSIZE,
    adapter_pool_maxsize: int = DEFAULT_POOLSIZE,
    adapter_max_retries: typing.Union[Retry, int] = DEFAULT_RETRIES,
    adapter_pool_block: bool = DEFAULT_POOLBLOCK,
):
    def requests_http_connection_factory(*args, **kwargs):
        connection = connection_factory(*args, **kwargs)
        connection.session.mount(
            prefix='https://',
            adapter=HTTPAdapter(
                pool_connections=adapter_pool_connections,
                pool_maxsize=adapter_pool_maxsize,
                max_retries=adapter_max_retries,
                pool_block=adapter_pool_block,
            )
        )
        connection.session.mount(
            prefix='http://',
            adapter=HTTPAdapter(
                pool_connections=adapter_pool_connections,
                pool_maxsize=adapter_pool_maxsize,
                max_retries=adapter_max_retries,
                pool_block=adapter_pool_block,
            )
        )
        return connection
    return requests_http_connection_factory
