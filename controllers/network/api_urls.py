import asyncio, aiohttp, time, requests
from controllers.network.fetch_data import async_request

API_BASE_URL = 'https://codeforces.com/api/'
CONTEST_BASE_URL = 'https://codeforces.com/contest/'
CONTESTS_BASE_URL = 'https://codeforces.com/contests/'
PROFILE_BASE_URL = 'https://codeforces.com/profile/'

class contest:
    def list(self, gym='false'):
        url = API_BASE_URL + 'contest.list?gym=' + gym
        return url

    def ratingChanges(self, contest_id):
        url = API_BASE_URL + 'contest.ratingChanges?contestId=' + str(contest_id)
        return url

    def standings(self,contest_id):
        url = API_BASE_URL + 'contest.standings?contestId=' + str(contest_id)
        return url

class user:
    def ratedList(self,contest_id, activeOnly):
        url = API_BASE_URL + 'user.ratedList?activeOnly='+activeOnly
        return url

    # Single Request
    def info(self, cf_handle):
        res = requests.get(API_BASE_URL + 'user.info?handles=' + cf_handle)
        res.encoding = 'utf-8'
        return res.json()

class clist:
    def contests(self):
        try:
            # Implement Async Clist API Call
            resp = requests.get('https://clist.by/api/v1/json/contest/?limit=500&order_by=-start', headers= {
                'Authorization': 'ApiKey joynahiid:339ccb7ec3e1dff04de10312f4d8811c0ad7c35a'
            })

            return resp.json()
        except Exception as e:
            print('api_clist', e)

contest_api = contest()
user_api = user()
clist_api = clist()

# loop = asyncio.get_event_loop()

# loop.run_until_complete(contest_api.list())