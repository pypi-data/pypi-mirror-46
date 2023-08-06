# -*- coding: utf-8 -*-

"""Client for reading data from Statnett REST API
"""

import json
import requests

import pandas as pd
from pandas.io.json import json_normalize

from statnett_api_client import config
from statnett_api_client.constants import OutputFmt, Topic


class Client(object):
    """Requesting and formatting Nordic power balance data from REST API
    """
    def __init__(self, uri=None, **kwargs):
        """
        :param uri: str, URI to send requests to
        :param fmt: {'json', 'pandas'}, format of returned object
        :param date2index, boolean, if True then set index using dates (valid only with fmt='pandas')
        :param time_cet, boolean, if True then add CET time (Central European Time),
            by default, time is UTC (valid only with fmt='pandas')
        """
        if uri is None:
            self.uri = config.URI

        self.fmt = str.lower(kwargs.get('fmt', 'json'))
        self.date2index = kwargs.get('date2index', False)
        self.time_cet = kwargs.get('time_cet', False)

    def get(self, topic, endpoint=None):
        """Requesting data for specific endpoint and return formatting data

        :param topic: {'balance', 'flow'}
        :param endpoint: str, URL's endpoint, e.g 'PhysicalFlowMap/GetFlow',
            if not specified then corresponding default endpoint is used

        :return: formatted data
        """
        data = None
        topic = config.topics[str.lower(topic)]

        # request data from API
        if endpoint is not None:
            response = requests.get(self.__make_url(self.uri, endpoint))
        else:
            response = requests.get(self.__make_url(self.uri, self.__get_endpoint(topic)))

        if self.__is_valid_response(response):
            try:
                # convert data to output format
                data = self.__format_response(topic, response)
            except ValueError:
                return None

        return data

    def __format_response(self, topic, response):
        """convert topic contents to output format
        """
        if self.fmt == OutputFmt.json.value:
            return self.__to_json(response)
        elif self.fmt == OutputFmt.pandas.value:
            return self.__to_pandas(topic, response)
        return None

    def __to_json(self, response):
        """convert to json array
        """
        if self.__is_json(response.text):
            return response.text
        return None

    def __to_pandas(self, topic, response):
        """convert to pandas dataframe
        """
        if topic['name'] == Topic.balance.value:
            parsed = self.__balance_to_pandas(topic, json.loads(response.text))
        elif topic['name'] == Topic.flow.value:
            parsed = self.__flow_to_pandas(topic, json.loads(response.text))
        else:
            raise ValueError

        if self.time_cet:
            parsed['date_cet'] = parsed['date_utc'].dt.tz_localize('UTC').dt.tz_convert('CET')

        if self.date2index:
            parsed.set_index('date_utc', inplace=True)

        return parsed

    def __balance_to_pandas(self, topic, json_response):
        # extract headers from json
        headers = json_normalize(json_response, record_path=topic['headers'])
        # get zone names from headers
        parsed = self.__headers_to_zones(headers)
        # add timestamp
        parsed['date_utc'] = pd.to_datetime(json_response[topic['date_var']], unit='ms')

        for record in topic['records']:
            # extract specific record from json
            rec = json_normalize(json_response, record_path=[record])
            rec.rename(columns={'value': record}, inplace=True)
            # convert values to numeric
            rec[record] = self.__to_numeric(rec[record])
            # add record to output
            parsed = parsed.merge(rec[[record]], left_index=True, right_index=True, how='left')

        parsed.reset_index(drop=True, inplace=True)

        return parsed

    @staticmethod
    def __flow_to_pandas(topic, json_response):
        parsed = json_normalize(json_response)
        # convert timestamp to datetime
        parsed['date_utc'] = pd.to_datetime(parsed[topic['date_var']], unit='ms')

        return parsed

    @staticmethod
    def __headers_to_zones(headers):
        zones = headers.copy().query('value != ""')
        zones.rename(columns={'value': 'zone'}, inplace=True)
        return zones[['zone']]

    @staticmethod
    def __to_numeric(series):
        """remove all non-numeric characters from pandas series and convert in to numeric
        """
        return pd.to_numeric(series.str.replace(r'\D', ''), errors='coerce')

    @staticmethod
    def __is_valid_response(response):
        return response.ok and hasattr(response, 'text')

    @staticmethod
    def __make_url(uri, endpoint):
        return uri + '/' + endpoint

    @staticmethod
    def __get_endpoint(topic):
        return topic['endpoint']

    @staticmethod
    def __is_json(obj):
        try:
            _ = json.loads(obj)
        except ValueError:
            return False
        return True
