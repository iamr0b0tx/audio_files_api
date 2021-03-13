class InvalidAudioType(Exception):
    def __init__(self, message="AudioType is not recognized!"):
        super(InvalidAudioType, self).__init__(message)


class AudioDoesNotExist(Exception):
    def __init__(self, message="AudioFile Object does not Exist!"):
        super(AudioDoesNotExist, self).__init__(message)
