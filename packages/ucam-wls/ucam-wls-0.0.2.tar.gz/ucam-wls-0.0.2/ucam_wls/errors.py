class WLSError(Exception):
    "A generic error occurred in the web login service."

class InvalidAuthRequest(WLSError):
    "An invalid authentication request was received from a WAA."

class SignatureNeeded(WLSError):
    "The WLS response needs signing before further handling can be done."

class CannotHandleRequest(WLSError):
    "The web login service cannot handle the WAA request for an unspecified reason."

class ProtocolVersionUnsupported(CannotHandleRequest):
    "The web login service does not support the protocol version requested by the WAA."

class NoMutualAuthType(CannotHandleRequest):
    "The web login service does not support any of the authentication types requested by the WAA."
