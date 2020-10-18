import requests, time, asyncio
from controllers.rating_calculator import CodeforcesRatingCalculator
from controllers.network.api_urls import contest_api, user_api
from controllers.network.fetch_data import async_request

CF_CONTEST_URL = 'https://codeforces.com/api/contest.standings'

class ratingChangeControl:
    def __init__(self, username, contest_id, sender, db):
        self.db = db
        if not contest_id: self.save_state = asyncio.create_task(self.get_latest_contestid())
        self.contest_id = contest_id

        if sender: self.sender = sender

        self.error = ratingChangeError()

        if username: self.username = str(username).lower()
        else: self.get_cf_handle()

        print(self.contest_id, self.username)

    # Message Generator
    async def fetch_rating_change_message(self):
        try:
            if self.contest_id == None:
                await self.save_state
                if self.contest_id == None:
                    return 'Couldn\'t fetch last rated contest. Codeforces didn\'t respond :/'

            if self.username == None:
                return self.error.usernameNotFound()['error']

            data = await asyncio.create_task(self.generate_rating_change())

            if 'error' in data: return data['error']

            if 'official' in data:
                oldRating, delta, contest_name = data['official']
                msg = '{} ' + str(oldRating) + ' to ' + str(oldRating+delta) + ' [{}' + str(delta) + ']'

                build_msg = contest_name, msg.format('Rating changed from', '+' if delta>=0 else '')

                return build_msg

            if 'prediction' in data:
                oldRating, delta, contest_name = data['prediction']
                msg = '{} ' + str(oldRating) + ' to ' + str(oldRating+delta) + ' [{}' + str(delta) + ']'
                
                build_msg = contest_name, msg.format('Predicting ', '+' if delta>=0 else '')

                return build_msg
        except Exception as e:
            print('Fetching Rating Error: ', e)
            pass

        return None


    # Last Contest if Contest ID was not given
    async def get_latest_contestid(self):
        try:
            url = contest_api.list()
            lis = await asyncio.create_task(async_request.unit_call(url))

            for i in lis['result']:
                if i['phase'] != 'BEFORE' and 'unrated' not in i['name'].lower():
                    self.contest_id = str(i['id'])
                    break
                
        except Exception as e:
            self.contest_id = None
            print("Couldn't fecth contest", e)


    # Get CF Handle if not given
    def get_cf_handle(self):
        try:
            self.username = self.db.collection('profiles').document(self.sender).get().to_dict()['username']
        except Exception as e:
            print('Database error',e)
            self.username = None
    
    # Generate Rating Change
    async def generate_rating_change(self):
        try:
            past = time.time()
            
            # rating_change_url = contest_api.ratingChanges(self.contest_id)

            # async_request.clear_urls()
            # async_request.add_url(rating_change_url)

            # rating_changed = await asyncio.create_task(async_request.call())
            # rating_changed = rating_changed[0]

            # if rating_changed['status'] == 'OK' and rating_changed['result']:
            #     for user in rating_changed['result']:
            #         if user['handle'].lower() == self.username:
            #             res = {'official' : (user['oldRating'], user['newRating']-user['oldRating'], user['contestName'])}
            #             return res
                
            #     return self.error.userNotRated(self.username) #Didn't Participate or rated
            # else:
            #     if 'comment' in rating_changed and 'finished yet' not in rating_changed['comment']:
            #         return  self.error.invalidContestID() # Invalid Contest

            rated_userlist_url = user_api.ratedList(self.contest_id,'true')
            current_ranklist_url = contest_api.standings(self.contest_id)

            async_request.clear_urls()
            async_request.add_url(rated_userlist_url)
            async_request.add_url(current_ranklist_url)

            rated_userlist, current_ranklist = await asyncio.create_task(async_request.call())

            current_rating = {}

            for user in rated_userlist['result']:
                current_rating[user['handle'].lower()] = user['rating']

            data = []

            print(rated_userlist['status'])
            print(current_ranklist['status'])

            for user in current_ranklist['result']['rows']:
                handle = user['party']['members'][0]['handle'].lower()

                if handle not in current_rating:
                    current_rating[handle] = 1500

                if current_rating[handle]>=2100 and 'Educational' in current_ranklist['result']['contest']['name']: continue
                    
                data.append({
                    'handle': handle,
                    'points': float(user['points']),
                    'penalty': int(user['penalty']),
                    'rating': int(current_rating[handle])
                })

            calculate = CodeforcesRatingCalculator(data)

            predicted_rating_change = calculate.calculate_rating_changes()

            future = time.time()

            print('Executed in', future-past, 'seconds')

            contest_name = current_ranklist['result']['contest']['name']

            if self.username in predicted_rating_change:
                res = {'prediction' : (current_rating[self.username], predicted_rating_change[self.username], contest_name)}
                return res

            else: return self.error.userNotRated(self.username) # Not rated or didn't participate

        except Exception as e:
            print('Rating Change Error', e)
            pass

        return None

# rating = makeRatingChangeMessage(1408, 'joynahiid')

# print(rating.fetch_rating_change())

class ratingChangeError:
    def usernameNotFound(self):
        text = {'error' : ('Codeforces Handle was not found.', 'Please send \'Remember <YOURCFHANDLE>\' to perform this query')}
        return text

    def invalidContestID(self):
        text = {'error' : 'Invalid Contest ID. Please send contest ID from the contest URL/ Link'}
        return text
    
    def userNotRated(self, username):
        text = {'error' : '{} was not rated or didn\'t participate'.format(username)}
        return text



# loop = asyncio.get_event_loop()
# test = ratingChangeControl('joynahiid','1421','','')

# got = loop.run_until_complete(test.generate_rating_change())

# print(got)