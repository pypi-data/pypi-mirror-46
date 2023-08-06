class UnauthorizedFileAccessException(BaseException):
    MESSAGE_PATTERN = 'You are not authorized to access {}'

    def __init__(self, file_path):
        global MESSAGE_PATTERN
        BaseException.__init__(self, MESSAGE_PATTERN.format(file_path))
