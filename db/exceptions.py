class UpdateError(Exception):
    def __init__(self, message="There was an Error during update!"):
        super(UpdateError, self).__init__(message)


class DeleteError(Exception):
    def __init__(self, message="There was an Error during deletion!"):
        super(DeleteError, self).__init__(message)


class AudioDoesNotExist(Exception):
    def __init__(self, message="AudioFile Object does not Exist!"):
        super(AudioDoesNotExist, self).__init__(message)
