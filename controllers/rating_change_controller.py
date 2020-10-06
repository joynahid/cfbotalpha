import requests, time
from controllers.rating_calculator import CodeforcesRatingCalculator
from controllers.api_requests import contestApi, userApi

CF_CONTEST_URL = 'https://codeforces.com/api/contest.standings'

class ratingChangeControl:
    def __init__(self, username, contest_id, sender, db):
        self.db = db

        if contest_id == None: self.get_latest_contestid()
        else: self.contest_id = str(contest_id)

        if sender: self.sender = sender

        self.error = ratingChangeError()

        if username: self.username = str(username).lower()
        else: self.get_cf_handle()

        print(self.contest_id, self.username)

    # Message Generator
    def fetch_rating_change_message(self):
        try:
            if self.contest_id == None:
                return 'Couldn\'t fetch last rated contest. Codeforces didn\'t respond :/'

            if self.username == None:
                return self.error.usernameNotFound()['error']

            data = self.generate_rating_change()

            if 'error' in data: return data['error']

            print(data)

            if 'official' in data:
                oldRating, delta, contest_name = data['official']
                msg = '{} ' + str(oldRating) + ' to ' + str(oldRating+delta) + ' [{}' + str(delta) + ']'

                build_msg = contest_name, msg.format('Rating changed from', '+' if delta>=0 else '')

                return build_msg

            if 'prediction' in data:
                oldRating, delta, contest_name = data['official']
                msg = '{} ' + str(oldRating) + ' to ' + str(oldRating+delta) + ' [{}' + str(delta) + ']'
                
                build_msg = contest_name, msg.format('Predicting', '+' if delta>=0 else '')

                return build_msg
        except Exception as e:
            print('Rating Change Controller ', e)
            pass

        return None

    # Last Contest if Contest ID was not given
    def get_latest_contestid(self):
        try:
            lis = contestApi.list()
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
            print(self.db)
            self.username = self.db.collection('profiles').document(self.sender).get().to_dict()['username']
        except Exception as e:
            print('Database error',e)
            self.username = None
    
    # Generate Rating Change
    def generate_rating_change(self):
        try:
            past = time.time()
            
            is_rating_changed = contestApi.ratingChanges(self.contest_id)

            if is_rating_changed['status'] == 'OK' and is_rating_changed['result']:
                for user in is_rating_changed['result']:
                    if user['handle'].lower() == self.username:
                        res = {'official' : (user['oldRating'], user['newRating']-user['oldRating'], user['contestName'])}
                        return res
                
                return self.error.userNotRated(self.username) #Didn't Participate or rated
            else:
                if 'comment' in is_rating_changed and 'finished yet' not in is_rating_changed['comment']:
                    return  self.error.invalidContestID() # Invalid Contest

            rated_userlist = userApi.ratedList(self.contest_id,'true', self.sender)
            print('success ratedList')
            current_ranklist = contestApi.standings(self.contest_id)
            print('success standings')

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