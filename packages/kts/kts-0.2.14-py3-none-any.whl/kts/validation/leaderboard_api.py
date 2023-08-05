import pandas as pd
from ..storage import cache

class LeaderboardApi:
    def __init__(self):


    def pprint(self):
        return pd.DataFrame()


leaderboard_api = LeaderboardApi()


# PUT TO kts/__init__.py
import mprop

@property
def leaderboard(kek):
    return leaderboard_api.pprint()

@property
def lb(kek):
    return leaderboard_api.pprint()

mprop.init()