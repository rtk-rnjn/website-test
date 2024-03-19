from __future__ import annotations

_400_ERRORS = {
    404: {
        "short_desc": "Not Found",
        "long_desc": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
    },
    400: {
        "short_desc": "Bad Request",
        "long_desc": "The request cannot be fulfilled due to bad syntax.",
    },
    401: {
        "short_desc": "Unauthorized",
        "long_desc": "The request has not been applied because it lacks valid authentication credentials for the target resource.",
    },
    403: {
        "short_desc": "Forbidden",
        "long_desc": "The server understood the request, but is refusing to fulfill it.",
    },
    405: {
        "short_desc": "Method Not Allowed",
        "long_desc": "The method specified in the request is not allowed for the resource identified by the request URI.",
    },
    406: {
        "short_desc": "Not Acceptable",
        "long_desc": "The resource identified by the request is only capable of generating response entities which have content characteristics not acceptable according to the accept headers sent in the request.",
    },
    408: {
        "short_desc": "Request Timeout",
        "long_desc": "The server timed out waiting for the request.",
    },
    415: {
        "short_desc": "Unsupported Media Type",
        "long_desc": "The server is refusing to service the request because the entity of the request is in a format not supported by the requested resource for the requested method.",
    },
    429: {
        "short_desc": "Too Many Requests",
        "long_desc": "The user has sent too many requests in a given amount of time.",
    },
}

_500_ERRORS = {
    500: {
        "short_desc": "Internal Server Error",
        "long_desc": "The server has encountered a situation it doesn't know how to handle.",
    },
    501: {
        "short_desc": "Not Implemented",
        "long_desc": "The request method is not supported by the server and cannot be handled.",
    },
    502: {
        "short_desc": "Bad Gateway",
        "long_desc": "The server, while acting as a gateway or proxy, received an invalid response from the upstream server it accessed in attempting to fulfill the request.",
    },
    503: {
        "short_desc": "Service Unavailable",
        "long_desc": "The server is currently unable to handle the request due to a temporary overloading or maintenance of the server.",
    },
    504: {
        "short_desc": "Gateway Timeout",
        "long_desc": "The server, while acting as a gateway or proxy, did not receive a timely response from the upstream server specified by the URI.",
    },
    505: {
        "short_desc": "HTTP Version Not Supported",
        "long_desc": "The server does not support the HTTP protocol version used in the request.",
    },
}

ERROR_CODES = _400_ERRORS | _500_ERRORS
