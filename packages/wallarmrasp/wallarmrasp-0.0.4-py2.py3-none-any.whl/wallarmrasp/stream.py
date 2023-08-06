try:
    from StringIO import StringIO as BytesBuffer  # Python 2.x
except BaseException:
    from io import BytesIO as BytesBuffer         # Python 3.x


class BufStream(object):
    def __init__(self, stream, buffered):
        self.stream = stream
        self.stream_buf = BytesBuffer(buffered)
        self.stream_buf_len = len(buffered)

    def read(self, size):
        result = b''
        if self.stream_buf_len:
            if size > self.stream_buf_len:
                result += self.stream_buf.read(self.stream_buf_len)
                self.stream_buf.close()
                self.stream_buf_len = 0
                size -= self.stream_buf_len
            else:
                result = self.stream_buf.read(size)
                self.stream_buf_len -= size
                return result
        return result + self.stream.read(size)

    def readline(self):
        if self.stream_buf_len:
            result = self.stream_buf.readline()
            self.stream_buf_len -= len(result)
            if self.stream_buf_len is 0:
                self.stream_buf.close()
            return result
        return self.stream.readline()

    def readlines(self, hint=1):
        return "\n".join([self.readline()] * hint)

    def __iter__(self):
        yield self.readline()

    def close(self):
        if self.stream_buf_len:
            self.stream_buf_len = 0
            self.stream_buf.close()

    def __del__(self):
        self.close()
