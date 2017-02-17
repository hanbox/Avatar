# -*- coding: utf-8 -*-

"""a simple facepp sdk
example:
api = API(key, secret)
api.detect(img = File('/tmp/test.jpg'))"""

__all__ = ['File', 'APIError', 'API']


DEBUG_LEVEL = 1

import sys
import socket
import urllib2
import json
import os.path
import itertools
import mimetools
import mimetypes
import time
import tempfile
from collections import Iterable


class File(object):

    """an object representing a local file"""
    path = None
    content = None

    def __init__(self, path):
        self.path = path
        self._get_content()

    def _get_content(self):
        """read image content"""

        if os.path.getsize(self.path) > 2 * 1024 * 1024:
            raise APIError(-1, None, 'image file size too large')
        else:
            with open(self.path, 'rb') as f:
                self.content = f.read()

    def get_filename(self):
        return os.path.basename(self.path)


class APIError(Exception):
    code = None
    """HTTP status code"""

    url = None
    """request URL"""

    body = None
    """server response body; or detailed error information"""

    def __init__(self, code, url, body):
        self.code = code
        self.url = url
        self.body = body

    def __str__(self):
        return 'code={s.code}\nurl={s.url}\n{s.body}'.format(s=self)

    __repr__ = __str__


class API(object):
    key = None
    secret = None
    server = 'https://api-cn.faceplusplus.com/facepp/v3/'

    decode_result = True
    timeout = None
    max_retries = None
    retry_delay = None

    def __init__(self, key, secret, srv=None,
                 decode_result=True, timeout=30, max_retries=10,
                 retry_delay=5):
        """:param srv: The API server address
        :param decode_result: whether to json_decode the result
        :param timeout: HTTP request timeout in seconds
        :param max_retries: maximal number of retries after catching URL error
            or socket error
        :param retry_delay: time to sleep before retrying"""
        self.key = key
        self.secret = secret
        if srv:
            self.server = srv
        self.decode_result = decode_result
        assert timeout >= 0 or timeout is None
        assert max_retries >= 0
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        _setup_apiobj(self, self, [])

    def update_request(self, request):
        """overwrite this function to update the request before sending it to
        server"""
        pass


def _setup_apiobj(self, api, path):
    if self is not api:
        self._api = api
        self._urlbase = api.server + '/'.join(path)

    lvl = len(path)
    done = set()
    for i in _APIS:
        if len(i) <= lvl:
            continue
        cur = i[lvl]
        if i[:lvl] == path and cur not in done:
            done.add(cur)
            setattr(self, cur, _APIProxy(api, i[:lvl + 1]))


class _APIProxy(object):
    _api = None
    """underlying :class:`API` object"""

    _urlbase = None

    def __init__(self, api, path):
        _setup_apiobj(self, api, path)

    def __call__(self, *args, **kargs):
        if len(args):
            raise TypeError('Only keyword arguments are allowed')
        form = _MultiPartForm()
        for (k, v) in kargs.iteritems():
            if isinstance(v, File):
                form.add_file(k, v.get_filename(), v.content)

        url = self._urlbase
        for k, v in self._mkarg(kargs).iteritems():
            form.add_field(k, v)

        request = urllib2.Request(url)
        body = str(form)
        request.add_header('Content-type', form.get_content_type())
        request.add_header('Content-length', str(len(body)))
        request.add_data(body)

        self._api.update_request(request)

        retry = self._api.max_retries
        while True:
            retry -= 1
            try:
                ret = urllib2.urlopen(request, timeout=self._api.timeout).read()
                break
            except urllib2.HTTPError as e:
                raise APIError(e.code, url, e.read())
            except (socket.error, urllib2.URLError) as e:
                if retry < 0:
                    raise e
                _print_debug('caught error: {}; retrying'.format(e))
                time.sleep(self._api.retry_delay)

        if self._api.decode_result:
            try:
                ret = json.loads(ret)
            except:
                raise APIError(-1, url, 'json decode error, value={0!r}'.format(ret))
        return ret

    def _mkarg(self, kargs):
        """change the argument list (encode value, add api key/secret)
        :return: the new argument list"""
        def enc(x):
            if isinstance(x, unicode):
                return x.encode('utf-8')
            return str(x)

        kargs = kargs.copy()
        kargs['api_key'] = self._api.key
        kargs['api_secret'] = self._api.secret
        for (k, v) in kargs.items():
            if isinstance(v, Iterable) and not isinstance(v, basestring):
                kargs[k] = ','.join([enc(i) for i in v])
            elif isinstance(v, File) or v is None:
                del kargs[k]
            else:
                kargs[k] = enc(v)

        return kargs


# ref: http://www.doughellmann.com/PyMOTW/urllib2/
class _MultiPartForm(object):

    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, content, mimetype=None):
        """Add a file to be uploaded."""
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, content))
        return

    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend(
            [part_boundary,
             'Content-Disposition: form-data; name="%s"' % name,'',value, ]
            for name, value in self.form_fields
        )

        # Add the files to upload
        parts.extend(
            [part_boundary,
             'Content-Disposition: file; name="%s"; filename="%s"' %
             (field_name, filename),
             'Content-Type: %s' % content_type,
             '',
             body,
             ]
            for field_name, filename, content_type, body in self.files
        )

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)


def _print_debug(msg):
    if DEBUG_LEVEL:
        sys.stderr.write(str(msg) + '\n')

_APIS = [
    '/detect',
    '/compare',
    '/search',
    '/faceset/create',
    '/faceset/addface',
    '/faceset/removeface',
    '/faceset/update',
    '/faceset/getdetail',
    '/faceset/delete',
    '/faceset/getfacesets',
    '/face/analyze',
    '/face/getdetail',
    '/face/setuserid'
]

_APIS = [i.split('/')[1:] for i in _APIS]
