from smsframework.exc import ProviderError, RequestError


class AfricasTalkingProviderError(ProviderError):

    def __init__(self, message):
        super().__init__(message)
