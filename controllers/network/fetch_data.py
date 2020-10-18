import asyncio
import aiohttp

class reqHandler:
    def __init__(self):
        self.urls = []

    def add_url(self, url):
        self.urls.append(url)

    def clear_urls(self):
        self.urls.clear()

    async def fetch(self, url, session):
        async with session.get(url) as response:
                return await response.json()

    async def call(self):
        async with aiohttp.ClientSession() as session:
            tasks = []

            for i in self.urls:
                task = asyncio.create_task(self.fetch(i, session))
                tasks.append(task)

            response = await asyncio.gather(*tasks)
            return response

    async def unit_call(self, url):
        async with aiohttp.ClientSession() as session:
            return await asyncio.create_task(self.fetch(url,session))

async_request = reqHandler()

# loop = asyncio.get_event_loop()
# obj = reqHandler()
# obj.add_url('https://google.com')
# loop.run_until_complete(obj.call())