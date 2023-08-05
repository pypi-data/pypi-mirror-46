from generic_sports_dataio_client import GenericSportsDataIOClient


class SportsClientNBA (GenericSportsDataIOClient):
    def __init__(self, customHttpClient=None):
        super().__init__(customHttpClient)

    def getSport(self):
        return 'nba'
