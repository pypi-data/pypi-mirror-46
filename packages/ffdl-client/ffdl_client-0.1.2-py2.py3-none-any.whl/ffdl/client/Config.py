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


class Config:
    def __init__(self, api_endpoint=None, api_version='v1', version='2017-02-13', user=None, password=None, user_info=None):
        self._api_endpoint = api_endpoint
        self._api_version = api_version
        self._version = version
        self._user = user
        self._password = password
        self._user_info = user_info

    @property
    def api_endpoint(self):
        return self._api_endpoint

    @property
    def api_version(self):
        return self._api_version

    @property
    def version(self):
        return self._version

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def user_info(self):
        return self._user_info

    def is_valid(self):
        if not self._api_endpoint:
            raise ValueError('FfDL API endpoint is required')

        if not self._user:
            raise ValueError('FfDL user is required')

        if not self._user_info:
            raise ValueError('FfDL user info required')

        return True
