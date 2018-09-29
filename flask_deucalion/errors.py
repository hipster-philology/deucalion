class DeucalionException(Exception):
    """ Exception for Deucalion """
    def __init__(self, message):
        super(DeucalionException, self).__init__()
        self.message = message
        self.code = 500


class UnknownModel(DeucalionException):
    def __init__(self, message):
        super(UnknownModel, self).__init__(message)
        self.code = 404
