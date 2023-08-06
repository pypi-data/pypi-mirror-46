import copy
import base64
import requests
import json
import logging
import platform

from . import utils
from . import exceptions
from .config import __version__

log = logging.getLogger(__name__)


class Api(object):
    # User-Agent for HTTP request
    library_details = "requests {0}; python {1}".format(
        requests.__version__, platform.python_version())
    user_agent = "Pillar-Python-SDK/{0} ({1})".format(
        __version__, library_details)
    _api_singleton = None

    # Global session object to do HTTP requests.
    requests_session = requests.session()

    # HTTP headers that should always be sent with every request.
    global_headers = {}

    def __init__(self, options=None, **kwargs):
        """Create API object

        Usage::

            >>> from pillarsdk import Api
            >>> Api.Default(
                    endpoint="http://localhost:5000",
                    username='USERNAME',
                    password='PASSWORD'
                )
        """
        kwargs = utils.merge_dict(options, kwargs)

        self.endpoint = kwargs["endpoint"]
        self.username = kwargs["username"]
        self.password = kwargs["password"]
        self.token = kwargs["token"] if kwargs.get("token") else None
        self.options = kwargs

    @staticmethod
    def Default(**kwargs):
        """Initialize the API in a singleton style
        """
        if Api._api_singleton is None or kwargs:
            Api._api_singleton = Api(
                endpoint=kwargs.get("endpoint"),
                username=kwargs.get("username"),
                password=kwargs.get("password"),
                token=kwargs.get("token"))
        return Api._api_singleton

    def basic_auth(self, token=None):
        """Returns base64 encoded token. Used to encode credentials
        for retrieving the token.
        """
        if token:
            credentials = "%s:%s" % (token, self.password or '')
        else:
            credentials = "%s:%s" % (self.username, self.password)
        return base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")

    def get_token(self):
        """Generate new token by making a POST request
        """
        return self.token

    def request(self, url, method, body=None, headers=None, files=None):
        """Make HTTP call, formats response and does error handling.
        Uses http_call method in API class.
        :param files: Dictionary of files to be uploaded via POST
        """

        http_headers = utils.merge_dict(self.headers(), headers)

        if http_headers.get('Pillar-Request-Id'):
            log.info("Pillar-Request-Id: %s", http_headers['Pillar-Request-Id'])
        try:
            # Support for Multipart-Encoded file upload
            if files and method in ['POST', 'PUT', 'PATCH']:
                return self.http_call(
                    url, method,
                    data=body,
                    files=files,
                    headers=http_headers,
                    verify=True)
            else:
                http_headers['Content-Type'] = "application/json"
                return self.http_call(url, method,
                                      data=utils.dumps(body),
                                      headers=http_headers,
                                      verify=True)

        # Handle unauthorized token
        except exceptions.UnauthorizedAccess as error:
            raise error

    def http_call(self, url, method, **kwargs):
        """Makes a http call. Logs response information.
        """

        response = self.requests_session.request(method, url, **kwargs)
        content = self.handle_response(response, response.text)

        return content

    def handle_response(self, response, content):
        """Check HTTP response codes
        """
        status = response.status_code

        if 200 <= status <= 299:
            return json.loads(content) if content else {}

        exception = exceptions.exception_for_status(status)
        if exception:
            raise exception(response, content)

        raise exceptions.ConnectionError(response, content, "Unknown response code: %s" % status)

    def headers(self):
        """Default HTTP headers
        """
        token = self.get_token()

        headers = copy.deepcopy(self.global_headers)
        headers.update({
            # "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent
        })

        if token:
            headers['Authorization'] = (
                "Basic {0}".format(self.basic_auth(token=token)))

        return headers

    def get(self, action, headers=None):
        """Make GET request
        """
        return self.request(utils.join_url(self.endpoint, action), 'GET',
                            headers=headers)

    def post(self, action, params=None, headers=None, files=None):
        """Make POST request
        """
        return self.request(utils.join_url(self.endpoint, action), 'POST',
                            body=params, headers=headers, files=files)

    def put(self, action, params=None, headers=None):
        """Make PUT request
        """
        return self.request(utils.join_url(self.endpoint, action), 'PUT',
                            body=params, headers=headers)

    def patch(self, action, params=None, headers=None, files=None):
        """Make PATCH request
        """
        return self.request(utils.join_url(self.endpoint, action), 'PATCH',
                            body=params, headers=headers, files=files)

    def delete(self, action, headers=None):
        """Make DELETE request
        """
        return self.request(utils.join_url(self.endpoint, action), 'DELETE',
                            headers=headers)

    def OPTIONS(self, action, headers=None):
        """Make OPTIONS request.

        Contrary to other requests, this method returns the raw requests.Response object.

        :rtype: requests.Response
        """

        http_headers = utils.merge_dict(self.headers(), headers)
        url = utils.join_url(self.endpoint, action)
        response = self.requests_session.request('OPTIONS', url, headers=http_headers)

        if 200 <= response.status_code <= 299:
            return response

        exception = exceptions.exception_for_status(response.status_code)
        if exception:
            raise exception(response, response.text)

        raise exceptions.ConnectionError(response, response.text,
                                         "Unknown response code: %s" % response.status_code)
