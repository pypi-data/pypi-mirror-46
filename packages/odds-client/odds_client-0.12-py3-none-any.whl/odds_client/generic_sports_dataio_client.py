from datetime import datetime, timedelta, date
from os import environ
from pprint import pprint
from urllib import request
from urllib.parse import urlencode
from default_http_client import DefaultHttpClient
from abc import ABCMeta, abstractmethod
import sys
import json


def getEnv(varName, defaultValue=None):
    return environ.get(varName) if environ.get(varName) else defaultValue


class GenericSportsDataIOClient:
    def __init__(self, customHttpClient=None):
        self.baseUrl = getEnv('SPORT_RADAR_BASE_URL',
                              'https://api.sportsdata.io/v3')
        self.secretKey = getEnv('SPORT_RADAR_SUBSCRIPTION_KEY')
        self.authHeader = 'Ocp-Apim-Subscription-Key'
        self.httpClient = customHttpClient if customHttpClient \
            else DefaultHttpClient()

    def __getAuthHeaders(self, headers={}):
        alteredHeaders = headers.copy()
        alteredHeaders[self.authHeader] = self.secretKey
        return alteredHeaders

    def __buildFuncURL(self, funcURL, **placeHolders):
        try:
            return self.baseUrl + funcURL % placeHolders
        except Exception as e:
            sys.stderr.write(repr(e) + "\n")
            return self.baseUrl

    def __doApiCall(self, fullURL, headers={}):
        authHeaders = self.__getAuthHeaders(headers)
        pprint(fullURL)
        response = self.httpClient.get(fullURL, authHeaders)
        return json.loads(response) if response else None

    def __dateRange(self, startDate, endDate):
        for n in range(int((endDate - startDate).days)):
            yield startDate + timedelta(n)

    @abstractmethod
    def getSport(self):
        return None

    def getPreGameOddsByDate(self, date=None):
        now = date if date else datetime.now().date().isoformat()
        sportName = self.getSport()
        fullURL = \
            self.__buildFuncURL('/%(sport)s/odds/json/'
                                'GameOddsByDate/%(date)s',
                                date=now, sport=sportName)
        response = self.__doApiCall(fullURL)
        return response

    def getPreGameOdds(self, startDate, endDate):
        preGames = None
        for sdate in self.__dateRange(startDate, endDate):
            data = self.getPreGameOddsByDate(sdate)
            if preGames is None:
                preGames = data
            else:
                for i in data:
                    preGames.append(i)
        return preGames
