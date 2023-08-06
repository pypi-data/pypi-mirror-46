
class PyOpenCellHTTPException(Exception):
    message = "Network problem accessing OpenCell API. Exception: \n {}"

    def __init__(self, error_msg):
        self.message = self.message.format(error_msg)
        super(PyOpenCellHTTPException, self).__init__(self.message)


class PyOpenCellServerErrorException(Exception):
    message = """Server ERROR in OpenCell API. \n
    A 50x response has been received from OpenCell API. \n
    Request: {verb} {url} \n
    Response: status={status} body={body}
    """

    def __init__(self, verb, url, status, body):
        self.message = self.message.format(verb=verb, url=url, status=status, body=body)
        super(PyOpenCellServerErrorException, self).__init__(self.message)
