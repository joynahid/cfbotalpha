import requests, time
from worker.calculator import CodeforcesRatingCalculator
from worker.codeforces_api import contest_api, user_api

CF_CONTEST_URL = 'https://codeforces.com/api/contest.standings'

class makeRatingChangeMessage:
    def __init__(self, username, contest_id = None):
        if contest_id == None:
            self.get_latest_contestid()
        else: self.contest_id = str(contest_id)

        self.username = str(username).lower()

        print(self.contest_id, self.username)

    def fetch_rating_change_message(self):
        try:
            data = self.generate_rating_change()

            contest_name = None

            if len(data)>3:
                contest_name = data[3]
                data = data[0:3]

            oldRating, delta, status = data

            contest_url = 'https://codeforces.com/contests/' + self.contest_id

            msg = '{} ' + str(oldRating) + ' to ' + str(oldRating+delta) + ' [{}' + str(delta) + ']'

            if status == 1: return contest_name, msg.format('Rating changed', '+' if delta>=0 else '')
            if status == 0: return contest_name, msg.format('Predicting ', '+' if delta>=0 else '')
            if status == 2: return 'I think the contest didn\'t start or invalid '
            if status == 4: return 'Noo', '{} didn\'t participate in this contest'.format(self.username)
            if status == 5: return '{} was not rated'.format(self.username)
        except:
            pass

        return None

    def get_latest_contestid(self):
        lis = contest_api.list()
        for i in lis['result']:
            if i['phase'] != 'BEFORE':
                self.contest_id = str(i['id'])
                break
    
    def generate_rating_change(self):
        try:
            past = time.time()
            
            is_rating_changed = contest_api.ratingChanges(self.contest_id)

            if is_rating_changed['status'] == 'OK':
                for user in is_rating_changed['result']:
                    if user['handle'].lower() == self.username:
                        return (user['oldRating'], user['newRating']-user['oldRating'], 1, user['contestName'])

                
                return (0,0,4) #Didn't Participate
            else:
                if 'comment' in is_rating_changed:
                    return (0,0,2)

            rated_userlist = user_api.ratedList(self.contest_id)
            print('success ratedList')
            current_ranklist = contest_api.standings(self.contest_id)
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
                return (current_rating[self.username], predicted_rating_change[self.username],0, contest_name)
            else: return (0,0,5)
        except Exception as e:
            print('Rating Change Error', e)
            pass
        finally:
            pass

        return None

# rating = makeRatingChangeMessage(1408, 'joynahiid')

# print(rating.fetch_rating_change())