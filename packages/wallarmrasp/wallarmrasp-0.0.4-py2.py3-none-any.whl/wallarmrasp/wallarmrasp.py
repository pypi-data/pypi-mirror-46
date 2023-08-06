import socket
import time
import logging
import sys

try:
    from wallarmrasp.sessionmanager import SessionManager
except BaseException:
    from .sessionmanager import SessionManager

try:
    from wallarmrasp.stream import BufStream
except BaseException:
    from .stream import BufStream

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

MODES = ['off', 'monitoring', 'block', 'aggressive']
MODES_OVERRIDE = ['on', 'off', 'strict']

SOCK_TIMEOUT_DEFAULT_MSEC = 10 * 10 ** 3  # 10 seconds
REQUEST_MAX_BODY_SIZE_DEFAULT = 100 * 10 ** 6  # 100MB
RESPONSE_MAX_BODY_SIZE_DEFAULT = 100 * 10 ** 6  # 100MB


class WallarmRASPMiddleware(object):
    _FINALIZE_FLAG = 1 << 0
    _LAST_FLAG = 1 << 1

    def __init__(self, application, mode='monitoring', **kwargs):
        """
        Create and initialize Wallarm RASP WSGI middleware. Options host, port
        or sock are required.

        Args:
            application: WSGI application
            mode (str, optional): Wallarm mode. (default: 'monitoring')

        Keyword Args:
            host (str): Wallarm RASP server hostname
            port (int): Wallarm RASP server port
            sock (str): Wallarm RASP server socket filename
            mode_override (str, optional): Wallarm mode override. (default: 'off')
            block_if_disconnected (bool, optional): Set to True if want to block page if connection to Wallarm RASP server is lost (default: False)
            sock_timeout_msec (int, optional): socket connection timeout with Wallarm RASP server (default: 10 seconds)
            request_max_body_size (int, optional): request max body size size that can be sent to Wallarm RASP server (default: 100MB)
            response_max_body_size (int, optional): response max body size size that can be sent to Wallarm RASP server (default: 100MB)
            block_headers (list of (header_name, header_value) tuples, optional): custom headers for block page
            block_body (list of str, optional): custom body for block page

        Returns:
            WSGI application with Wallarm RASP middleware.
        """
        if not mode in MODES:
            raise Exception(
                'invalid "mode" (supported {0})' % MODES)

        # mode override
        mode_override = kwargs.get('mode_override', 'off')
        if not mode_override in MODES_OVERRIDE:
            raise Exception(
                'invalid "mode_override" (supported {0})' % MODES_OVERRIDE)

        # getting socket parameters. UDS or TCP are supported.
        # used for connection to Wallarm RASP server
        if kwargs.get('host') and kwargs.get('port'):
            sock_param = {
                'family': socket.AF_INET,
                'address': (kwargs['host'], int(kwargs['port']))
            }
        elif kwargs.get('sock'):
            sock_param = {
                'family': socket.AF_UNIX,
                'address': kwargs['sock']
            }
        else:
            raise Exception('param "host", "port" or "sock" must be specified')

        # geting socket timeout parameters
        # this timeout use for connection to Wallarm RASP server
        sock_timeout_str = kwargs.get('sock_timeout_msec', None)
        if sock_timeout_str and int(sock_timeout_str) > 0:
            sock_timeout_msec = int(sock_timeout_str)
        else:
            sock_timeout_msec = SOCK_TIMEOUT_DEFAULT_MSEC

        # strip request body more than request_max_body_size
        request_max_body_size = kwargs.get(
            'request_max_body_size', REQUEST_MAX_BODY_SIZE_DEFAULT)

        # strip responce body more than response_max_body_size
        response_max_body_size = kwargs.get(
            'response_max_body_size', RESPONSE_MAX_BODY_SIZE_DEFAULT)

        # custom block headers
        block_headers = kwargs.get('block_headers', [])

        # custom block body
        block_body = kwargs.get('block_body', [b''])

        # block if connection to Wallarm RASP server is lost
        block_if_disconnected = kwargs.get('block_if_disconnected', False)

        self.application = application
        self.mode_index = MODES.index(mode)
        self.mode_override_index = MODES_OVERRIDE.index(mode_override)
        self.analyze = False if mode is 'off' else True
        self.block_if_disconnected = bool(block_if_disconnected)
        self.sock_param = sock_param
        self.sock_timeout = int(sock_timeout_msec) / 1000.0  # convert to usec
        self.request_max_body_size = int(request_max_body_size)
        self.response_max_body_size = int(response_max_body_size)
        self.block_headers = block_headers
        self.block_body = block_body

    def __call__(self, environ, start_response):
        if not self.analyze:
            return self.application(environ, start_response)
        block = self._analyze_request(environ)
        if block is None:
            # connection to Wallarm RASP server error
            logging.warning(
                'Wallarm RASP server send err: %s', self.sock_param['address'])
            if self.block_if_disconnected:
                return self._block_request(environ, start_response)
            else:
                return self.application(environ, start_response)
        if block is True:
            # we need block request
            return self._block_request(environ, start_response)
        # allow process orig request
        return self.application(environ, start_response)

    def _analyze_request(self, environ):
        conn = SessionManager(self.sock_param, self.sock_timeout)
        req_param = self._get_request_param(environ)
        try:
            conn.connect()
            return conn.send_request(req_param)
        except:
            logging.debug('send request status: %s', sys.exc_info())

            return None

    def _block_request(self, environ, start_response):
        start_response('403 FORBIDDEN', self.block_headers)
        return self.block_body

    def _get_request_param(self, environ):
        now = time.time()
        body, len_orig = _get_post_body(environ, self.request_max_body_size)
        return [
            0,  # request id
            self.mode_index,  # wallarm mode
            self.mode_override_index,  # wallarm mode override
            self._FINALIZE_FLAG | self._LAST_FLAG,  # request flags
            environ.get('wsgi.url_scheme', None),  # scheme
            environ.get('REQUEST_METHOD', None),  # method
            environ.get('SERVER_PROTOCOL', None),  # protocol
            environ.get('SERVER_ADDR', None),  # server addr
            environ.get('SERVER_PORT', None),  # server port
            environ.get('REMOTE_ADDR', None),  # remote addr
            environ.get('REMOTE_PORT', None),  # remote port
            now,  # start time
            now,  # end time
            _get_uri(environ),  # uri
            _get_headers(environ),  # headers
            body,  # body
            len_orig,  # body orig len
        ]


def _get_uri(environ):
    uri = ''

    if environ.get('HTTP_HOST'):
        uri += environ['HTTP_HOST']
    else:
        uri += environ.get('SERVER_NAME', '')

    uri += quote(environ.get('SCRIPT_NAME', ''))
    uri += quote(environ.get('PATH_INFO', ''))
    if environ.get('QUERY_STRING'):
        uri += '?' + environ['QUERY_STRING']
    return uri


def _get_headers(environ):
    headers = []
    for key in environ.keys():
        if key.startswith("HTTP_"):
            headers.append((key[5:].replace('_', '-'), environ[key]))
    if environ.get('CONTENT_TYPE'):
        headers.append(('CONTENT-TYPE', environ["CONTENT_TYPE"]))
    if environ.get('CONTENT_LENGTH'):
        headers.append(('CONTENT-LENGTH', environ["CONTENT_LENGTH"]))
    return headers


def _get_post_body(environ, max_len):
    try:
        content_length = int(environ.get('CONTENT_LENGTH', '-1'))
        if content_length == -1:
            transfer_encoding = environ.get('HTTP_TRANSFER_ENCODING', '')
            if transfer_encoding.lower().find('chunked') != -1:
                body = _read_post_body(environ, max_len)
                return body, len(body)
            else:
                return b'', None
        elif content_length > max_len:
            return _read_post_body(environ, max_len), content_length
        else:
            return _read_post_body(environ, content_length), None
    except ValueError:
        return b'', None


def _read_post_body(environ, read_len):
    body = environ['wsgi.input'].read(read_len)
    if not len(body):
        return b''
    environ['wsgi.input'] = BufStream(environ['wsgi.input'], body)
    return body
