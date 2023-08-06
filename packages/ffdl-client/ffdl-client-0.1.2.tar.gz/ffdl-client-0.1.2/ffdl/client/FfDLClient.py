#
# Copyright 2019 Luciano Resende
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import requests

from ffdl.client import Config
from requests.auth import HTTPBasicAuth


class FfDLClient:
    def __init__(self, config:Config):
        """
        :param config: FfDL connection configuration
        """
        self.config = config

    def get(self, url):
        """
        Submit a get request to a FfDL server
        :param url: the api url path
        :return: a json payload with the api result
        """
        # validate that proper configuration has been provided
        self.config.is_valid()

        # accomodate provided strings starting with '/'
        if url.startswith('/'):
            url = url[1:]

        endpoint = self._create_ffdl_endpoint(url)

        headers = {'accept': 'application/json',
                   'X-Watson-Userinfo': self.config.user_info}

        try:
            response = requests.get(endpoint,
                                  auth=HTTPBasicAuth(self.config.user, self.config.password),
                                  headers=headers)

            if not response:
                raise RuntimeError("Error submitting job to FfDL")

            return response

        except requests.exceptions.Timeout:
            print("FfDL Job Submission Request Timed Out....")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects were detected during job submission")
        except requests.exceptions.ConnectionError:
            print("Connection Error: Could not connect to {}".format(endpoint))
        except requests.exceptions.HTTPError as http_err:
            print("HTTP Error - {} ".format(http_err))
        except requests.exceptions.RequestException as err:
            print(err)

    def post(self, url, **file_paths):
        """
        Submit a post request to a FfDL server
        :param url: the api url path
        :param file_paths: files to submit with the post request
        :return: a json payload with the api result
        """
        # validate that proper configuration has been provided
        self.config.is_valid()

        # accomodate provided strings starting with '/'
        if url.startswith('/'):
            url = url[1:]

        endpoint = self._create_ffdl_endpoint(url)

        headers = {'accept': 'application/json',
                   'X-Watson-Userinfo': self.config.user_info}

        files = {}
        for name, path in file_paths.items():
            files[name] = open(file_paths[name], 'rb')

        try:
            result = requests.post(endpoint,
                                   auth=HTTPBasicAuth(self.config.user, self.config.password),
                                   headers=headers,
                                   files=files)

            return result.json()

        except requests.exceptions.Timeout:
            print("FfDL Job Submission Request Timed Out....")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects were detected during job submission")
        except requests.exceptions.ConnectionError:
            print("Connection Error: Could not connect to {}".format(endpoint))
        except requests.exceptions.HTTPError as http_err:
            print("HTTP Error - {} ".format(http_err))
        except requests.exceptions.RequestException as err:
            print(err)

        finally:
            for name, file in files.items():
                file.close()

    def _create_ffdl_endpoint(self, url):
        """
        Utility method to create the FfDL api url based on FfDL
        server endpoint, api version and model version
        :param url:
        :return:
        """
        return "{}/{}/{}?version={}".format(self.config.api_endpoint, self.config.api_version, url, self.config.version)
