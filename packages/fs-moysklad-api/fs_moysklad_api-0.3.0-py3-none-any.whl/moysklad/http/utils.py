from enum import Enum


DEBUG_RATE_HEADERS = {
    'X-RateLimit-Limit': 'true',
    'X-Lognex-Retry-TimeInterval': 'true',
    'X-RateLimit-Remaining': 'true',
    'X-Lognex-Reset': 'true',
    'X-Lognex-Retry-After': 'true',
}


class HTTPMethod(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'


class ApiResponse:
    def __init__(self, response, json_response) -> None:
        self.context = json_response['context']
        self.meta = json_response['meta']
        self.rows = json_response['rows']
        self.response = response
        self.headers = response.headers

    def __str__(self):
        return f'ApiResponse [{self.response.status_code}]'


class RequestConfig:
    def __init__(self, use_pos_api: bool = False,
                 use_pos_token: bool = False,
                 ignore_request_body: bool = False,
                 follow_redirects: bool = True,
                 format_millisecond: bool = False,
                 debug_rate_limit: bool = False) -> None:
        self.use_pos_api = use_pos_api
        self.use_pos_token = use_pos_token
        self.ignore_request_body = ignore_request_body
        self.follow_redirects = follow_redirects
        self.format_millisecond = format_millisecond
        self.debug_rate_limit = debug_rate_limit
