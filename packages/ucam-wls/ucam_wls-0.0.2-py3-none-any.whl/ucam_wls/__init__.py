"ucam_wls top-level module.  The entire public API is made available here."

from . import context, request, response, signing

from .context import AuthPrincipal, LoginService
from .request import AuthRequest
from .response import AuthResponse
from .signing import Key

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend


__all__ = ["context", "request", "response", "signing",
           "AuthPrincipal", "LoginService",
           "AuthRequest", "AuthResponse", "Key",
           "load_private_key"]


def load_private_key(path, kid, password=None):
    """
    Load a PEM-encoded private key from a given path, assigning it a specified
    key ID ('kid').  A password, if needed, can optionally be specified.

    :type path: Path-like object (can be :class:`str`)
    :param path:        The filesystem path to the private key file.

    :type kid: :class:`int`
    :param kid:         The key ID to assign to this private key.

    :type kid: :class:`bytes` or :class:`str`
    :param password:    The password, if needed, to decrypt the private key.
                        Should be :const:`None` if the key is not encrypted.
                        If password is given as a :class:`str`, it will be
                        decoded as UTF-8.

    Returns a :class:`ucam_wls.signing.Key` instance.
    """
    if not isinstance(kid, int):
        raise TypeError("kid must be an integer")
    if isinstance(password, str):
        password = password.decode()
    with open(path, 'rb') as f:
        key = load_pem_private_key(f.read(), password, default_backend())
    return Key(key, kid)
