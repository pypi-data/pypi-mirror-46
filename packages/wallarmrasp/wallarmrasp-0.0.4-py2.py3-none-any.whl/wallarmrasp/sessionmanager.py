import socket
import msgpack


class SessionManager(object):
    # Internal states
    S_CONNECT = 0
    S_VERSION = 1
    S_AUTH = 2
    S_SEND = 3

    # Message code definition
    MSG_CODE_VERSION = 1
    MSG_CODE_AUTH = 2
    MSG_CODE_HTTP_REQ = 3

    # Supported protocol version
    PROTO_VER = 1

    def __init__(self, param, timeout, auth_str=None):
        sock = socket.socket(family=param['family'])
        sock.settimeout(timeout)
        self.sock = sock
        self.addr = param['address']
        self.auth_str = auth_str
        self.state = self.S_CONNECT

    def __del__(self):
        self.close()

    def connect(self):
        if not self.state is self.S_CONNECT:
            return
        try:
            self.sock.connect(self.addr)
        except socket.error as err:
            raise Exception(
                'cannot connect to Wallarm server: {0}'.format(err))
        self.state = self.S_VERSION

    def close(self):
        if not self.state is self.S_CONNECT:
            return
        self.sock.close()

    def send_request(self, req_param={}):
        try:
            send_rawmsg = self._get_rawmsg(req_param)
            self.sock.sendall(send_rawmsg)

            recv_rawmsg = self.sock.recv(4096)
            return self._decode_rawmsg(recv_rawmsg)
        except socket.error as err:
            raise Exception('Wallarm server socket error: {0}'.format(err))

    def _get_rawmsg(self, req_param=[]):
        msg = []

        if self.state is self.S_CONNECT:
            Exception('not connection with Wallarm server')

        if self.state <= self.S_VERSION:
            msg.append([self.MSG_CODE_VERSION, self.PROTO_VER])

        if self.state < self.S_AUTH and self.auth_str:
            msg.append([self.MSG_CODE_AUTH, self.auth_str])

        if self.state < self.S_SEND:
            msg.append([self.MSG_CODE_HTTP_REQ, req_param])

        return msgpack.packb(msg)

    def _decode_rawmsg(self, raw_msg):
        msg = msgpack.unpackb(raw_msg)
        block = None
        for item in msg:
            msg_code = item[0]
            msg_data = item[1]
            if self.state is self.S_SEND:
                if not msg_code is self.MSG_CODE_HTTP_REQ:
                    Exception('wrong code: {0} for S_SEND'.format(msg_code))
                if not msg_data[0] is True:
                    Exception(
                        'request not be processed: {0}'.format(msg_data[0]))
                block = msg_data[1]  # block request flag
            elif self.state is self.S_VERSION:
                if not msg_code is self.MSG_CODE_VERSION:
                    Exception('wrong code: {0} for S_VERSION'.format(msg_code))
                version = msg_data  # version info
                if version is self.PROTO_VER:
                    self.state = self.S_AUTH if self.auth_str else self.S_SEND
                else:
                    Exception('protocol version error: #{0}'.format(version))
            elif self.state is self.S_AUTH:
                if not msg_code is self.MSG_CODE_AUTH:
                    Exception('wrong code: {0} for S_AUTH'.format(msg_code))
                auth_status = msg_data  # auth status info
                if auth_status is not True:
                    Exception('auth error: {0}'.format(auth_status))
                self.state = self.S_SEND
            else:
                Exception('unsupported code #{0} for state #{1}'.format(
                    msg_code, self.state))
        return block
