from flask import json
import requests
from worker.cacher import cacheMaster
from worker.facebook_api import facebook

API_BASE_URL = 'https://codeforces.com/api/'
CONTEST_BASE_URL = 'https://codeforces.com/contest/'
CONTESTS_BASE_URL = 'https://codeforces.com/contests/'
PROFILE_BASE_URL = 'https://codeforces.com/profile/'
DEFAULT_RATING = 1500

class contest:
    def list(self, gym='false'):
        url = API_BASE_URL + 'contest.list?gym=' + gym
        res = requests.get(url, stream = True)
        res.encoding = 'utf-8'
        return res.json()

    def ratingChanges(self, contest_id):
        cache = cacheMaster.retrieveCache(contest_id, 'contest_ratingChanges')
        if cache: return cache

        url = API_BASE_URL + 'contest.ratingChanges?contestId=' + str(contest_id)
        res = requests.get(url, stream = True)

        res.encoding = 'utf-8'

        cacheMaster.makeCache(contest_id, 'contest_ratingChanges', res)

        return res.json()

    def standings(self,contest_id):

        cache = cacheMaster.retrieveCache(contest_id, 'contest_standings')
        if cache: return cache

        url = API_BASE_URL + 'contest.standings?contestId=' + str(contest_id)
        res = requests.get(url, stream = True)

        res.encoding = 'utf-8'

        cacheMaster.makeCache(contest_id, 'contest_standings', res)
    
        return res.json()

class user:
    def ratedList(self,contest_id,activeOnly ='true'):

        cache = cacheMaster.retrieveCache(contest_id, 'user_ratedList')
        if cache: return cache

        facebook.send_message('Hold on a second')

        url = API_BASE_URL + 'user.ratedList?activeOnly='+activeOnly
        
        res = requests.get(url, stream = True)

        res.encoding = 'utf-8'

        # with  as res:
        #     local_filename = f"worker/chunkstore/{contest_id}_{'user_ratedList'}"
        #     res.raise_for_status()
        #     with open(local_filename, 'wb') as f:
        #         for chunk in res.iter_content(chunk_size=2000):
        #             f.write(chunk)

        cacheMaster.makeCache(contest_id, 'user_ratedList', res)

        return res.json()

contest_api = contest()
user_api = user()