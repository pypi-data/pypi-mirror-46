from sports_client_nba import SportsClientNBA


class SportsClientFactory():
    __instance_client_nba = None

    def __getIntanceClientNBA(self):
        if self.__instance_client_nba is None:
            self.__instance_client_nba = SportsClientNBA()
        return self.__instance_client_nba

    def getApiClient(self, sport):
        if sport == 'nba':
            return self.__getIntanceClientNBA()
