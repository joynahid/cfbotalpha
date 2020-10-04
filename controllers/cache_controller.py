from flask import json

BASE_LOCATION = "cache/"

class cacheHandler:
    def makeCache(self,contest_id, type_, response):
        filename = f'{contest_id}_{type_}_.json'
        try:
            print('making', filename)

            with open(BASE_LOCATION + filename, 'w', encoding="utf-8") as cache:
                cache.write(response.text)
        except Exception as e:
            print('cache making error', e)

    def retrieveCache(self,contest_id, type_):
        filename = f"{contest_id}_{type_}_.json"

        try:
            with open(BASE_LOCATION + filename, 'r', encoding='utf-8') as cache:
                return json.loads(cache.read())
        except Exception as e:
            print('retrieveError', e, type)
        
        return None

cacheMaster = cacheHandler()