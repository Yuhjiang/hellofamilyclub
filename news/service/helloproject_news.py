import asyncio

import aiohttp


async def fetch_news(session, url):
    async with session.get(url) as response:
        return await response.text()


async def collect_news(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch_news(session, url)
        with open('index.html', 'w') as f:
            print(html, file=f)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(collect_news('http://www.helloproject.com/news/'))
