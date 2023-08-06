from urllib.parse import parse_qs, urlsplit, urlunsplit, urlencode

from .errors import InvalidAuthRequest, ProtocolVersionUnsupported

def clean_url(url):
    parts = urlsplit(url)
    if parts.scheme not in ['http', 'https']:
        raise InvalidAuthRequest("Invalid URL scheme")
    return url

class AuthRequest:
    "An authentication request sent by a WAA."

    REQUIRED_PARAMS = {'ver', 'url'}
    OPTIONAL_PARAMS = {'desc', 'aauth', 'iact', 'msg', 'params', 'date', 'skew', 'fail'}
    VALID_PARAMS = REQUIRED_PARAMS | OPTIONAL_PARAMS
    IGNORED_PARAMS = {'skew'}

    def __init__(self, ver, url, desc='', aauth='', iact='', msg='', params='',
                 date='', fail='', skew=None):
        self.ver = int(ver)
        self.url = clean_url(url)
        self.desc = desc

        if isinstance(aauth, list):
            self.aauth = aauth
        elif isinstance(aauth, str):
            self.aauth = aauth.split(',')
        elif aauth is None:
            self.aauth = []
        else:
            raise ValueError("Unparseable aauth value %r" % aauth)

        if isinstance(iact, bool):
            self.iact = iact
        elif iact == 'yes':
            self.iact = True
        elif iact == 'no':
            self.iact = False
        else:
            self.iact = None

        self.msg = msg
        self.params = params

        self.date = date

        if isinstance(fail, bool):
            self.fail = fail
        else:
            self.fail = (fail == 'yes')

    @property
    def params_dict(self):
        d = {k: getattr(self, k) for k in self.VALID_PARAMS - self.IGNORED_PARAMS}
        if self.iact == True:
            d['iact'] = 'yes'
        elif self.iact == False:
            d['iact'] = 'no'
        else:
            d['iact'] = ''
        d['fail'] = 'yes' if self.fail else ''
        d['aauth'] = ','.join(self.aauth)
        return d

    @classmethod
    def from_params_dict(cls, params_dict, check_supported=True, ignore_unknown=False):
        d = dict(params_dict)

        # Go from 1-long lists of values to just the values
        for k, v in d.items():
            if isinstance(v, list):
                d[k] = v[0]

        if cls.REQUIRED_PARAMS - set(d.keys()) != set():
            raise InvalidAuthRequest(
                "Missing required parameter(s): %s" %
                ', '.join(cls.REQUIRED_PARAMS - set(d.keys()))
            )

        extra_params = set(d.keys()) - (cls.VALID_PARAMS)
        if extra_params:
            if ignore_unknown:
                for k in extra_params:
                    del d[k]
            else:
                raise InvalidAuthRequest("Unknown parameter(s): %s" %
                                         ', '.join(extra_params))

        try:
            d['ver'] = int(d['ver'])
        except ValueError as e:
            raise InvalidAuthRequest("ver parameter is not an integer") from e

        req = cls(**d)
        if not req.data_valid:
            raise InvalidAuthRequest("Authentication request failed validation")

        if check_supported and not req.version_supported:
            raise ProtocolVersionUnsupported(d['ver'])

        return req

    @property
    def as_query_string(self):
        return urlencode(self.params_dict(), doseq=True)

    @classmethod
    def from_query_string(cls, query_string, *args, **kwargs):
        params_dict = parse_qs(query_string)

        for k, values in params_dict.items():
            if len(values) > 1:
                raise InvalidAuthRequest("Repeated parameter %s" % k)

        return cls.from_params_dict(params_dict, *args, **kwargs)

    @property
    def data_valid(self):
        result = all([
            isinstance(self.ver, int),
            isinstance(self.url, str),
            isinstance(self.desc, str),
            isinstance(self.aauth, list),
            isinstance(self.iact, bool) or self.iact is None,
            isinstance(self.msg, str) or self.msg is None,
            isinstance(self.params, str) or self.params is None,
            isinstance(self.fail, bool) or self.fail is None,
        ])
        if self.desc is not None:
            result = result and all([0x20 <= ord(c) <= 0x7e for c in self.desc])
        if self.msg is not None:
            result = result and all([0x20 <= ord(c) <= 0x7e for c in self.msg])
        return result

    @property
    def version_supported(self):
        return 1 <= self.ver <= 3
