import json
import os

import requests
from swiss_python.logger.log_utils import get_logger

from swiss_common_utils.json.json_utils import beautify_json
from swiss_common_utils.network.url.url_utils import add_http_if_missing


class SWISSServiceBase:
    logger = get_logger()

    HEADERS = {'Content-type': 'application/json'}

    def __init__(self, host, port=None, log_response=False):
        self._host = add_http_if_missing(host)
        self._port = port
        self._log_response = log_response

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    def _get_url(self, path_params_list=None, request_params_dict=None):
        url = self.host
        if self.port:
            url = url + ':' + self.port
        if path_params_list is not None:
            url = url.strip('/') + '/' + self.__build_url_path(path_params_list)
        if request_params_dict is not None:
            url = url + '?' + self.__build_url_parameters(request_params_dict)

        return url

    def __handle_response_code(self, response_code):
        self.logger.info('HTTP response code: ' + str(response_code))
        if response_code != 200:
            self.logger.error('HTTP response code description: ' + requests.status_codes._codes[response_code][0])

    def _handle_response(self, response):
        response_code = response.status_code

        self.__handle_response_code(response_code)

        response_elapsed_milli = int(round(response.elapsed.total_seconds() * 1000))
        self.logger.info('Request elapsed: ' + str(response_elapsed_milli) + 'ms')
        self.logger.info('Response headers: {}'.format(response.headers))
        response_content = response.content.decode('utf-8')
        response_content_json = json.loads(response_content)
        if self._log_response:
            self.logger.info('Response: \n' + beautify_json(response_content_json))
        return response_content_json

    def __build_url_path(self, path_params_list):
        return '/'.join(path_params_list)

    def __build_url_parameters(self, url_params_dict):
        key_val_list = []
        for key in url_params_dict:
            key_val_list.append(key + '=' + url_params_dict[key])

        return '&'.join(key_val_list)

    def dispatch(self, url, data=None):
        self.logger.info('### Sending request: ###')
        self.logger.info('URL: ' + url)

        # TODO: requests go through the proxy because of the env var. should find a workaround
        if data is None:
            self.logger.info('Method: GET')

            return requests.get(url=url, headers=self.HEADERS)
        else:
            self.logger.info('Method: POST')
            self.logger.info('Post data: {}'.format(data))
            return requests.post(url=url, headers=self.HEADERS, data=data)
