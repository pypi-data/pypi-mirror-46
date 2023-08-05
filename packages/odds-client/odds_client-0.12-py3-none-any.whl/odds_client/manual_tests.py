from pprint import pprint
from sports_client_factory import SportsClientFactory
from datetime import datetime, timedelta, date
import json

factory = SportsClientFactory()
sr = factory.getApiClient('nba')
print("\n Testing getPreGameOddsByDate \n")
data = sr.getPreGameOddsByDate()
pprint(data)

print("\n Testing getPreGameOdds \n")
start_date = date(2019, 5, 1)
end_date = date(2019, 5, 7)
data = sr.getPreGameOdds(start_date, end_date)
pprint(data)
