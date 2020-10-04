from worker.bot import commandProcessor

# Write tests here for testing the bot

bot = commandProcessor('remember hwyyou')
print(bot.find_and_execute_command())

bot = commandProcessor('rate 235 tourist')
print(bot.find_and_execute_command())

bot = commandProcessor('rate 1408', 4430672097006727)
print(bot.find_and_execute_command())

bot = commandProcessor('rate', 4430672097006727)
print(bot.find_and_execute_command())

bot = commandProcessor('help', 4430672097006727)
print(bot.find_and_execute_command())

# import asyncio, requests, time
# from aiohttp import ClientSession

# fut = time.time()

# tm = time.time()
# requests.get('https://codeforces.com/api/user.ratedList?activeOnly=true')
# requests.get('https://codeforces.com/api/contest.ratingChanges?contestId=566')

# print(time.time() - fut)

# async def fetch(url, session):
#     async with session.get(url) as response:
#         return await response.read()

# async def run(r):
#     tasks = []
#     fut = time.time()
#     # Fetch all responses within one Client session,
#     # keep connection alive for all requests.
#     async with ClientSession() as session:
#         task = asyncio.ensure_future(fetch('https://codeforces.com/api/user.ratedList?activeOnly=true', session))
#         tasks.append(task)
#         task = asyncio.ensure_future(fetch('https://codeforces.com/api/contest.ratingChanges?contestId=566', session))
#         tasks.append(task)

#         responses = await asyncio.gather(*tasks)
#         # you now have all response bodies in this variable
#         print('DONE')
    
#     print(time.time() - fut)

# def print_responses(result):
#     print(result)

# loop = asyncio.get_event_loop()
# future = asyncio.ensure_future(run(4))
# loop.run_until_complete(future)





























print('\n===========================\nAll test passed')