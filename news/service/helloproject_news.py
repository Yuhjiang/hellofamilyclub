import asyncio

import aiohttp
from bs4 import BeautifulSoup

from news.tasks import get_information_from_page_task

PREFIX = 'http://www.helloproject.com'


async def fetch_news(session, url):
    async with session.get(url) as response:
        return await response.text()


async def collect_news(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch_news(session, url)
        soup = BeautifulSoup(html, 'lxml')
        await fetch_news_from_html(soup)


async def fetch_news_from_html(soup):
    news_contents = get_news_contents(soup)
    news_lists = get_news_lists(news_contents)

    tasks = []
    categories = []
    for news in news_lists:
        news_url = news.find('a')['href']
        category = news.select('.icon-schedule')[0].string
        task = asyncio.create_task(get_news_detail(news_url))
        tasks.append(task)
        categories.append(category)
    await asyncio.wait(tasks)
    for i, task in enumerate(tasks):
        html, url = task.result()
        get_information_from_page_task.delay(html, url, categories[i])


def get_category(soup):
    category = soup.select('.icon-schedule')
    if category:
        return category[0].string
    else:
        return None


async def get_news_detail(url):
    url = PREFIX + url
    async with aiohttp.ClientSession() as session:
        html = await fetch_news(session, url)
        return html, url


def get_news_contents(soup):
    news_contents = soup.find(id='news_contents')
    return news_contents


def get_news_lists(news_contents):
    return news_contents.find_all('li')


async def collect_hello_project_all_news(start, end):
    tasks = []
    current = 0
    for page in range(start, end):
        url = PREFIX + '/news/?p={}'.format(page)
        task = asyncio.create_task(collect_news(url))
        tasks.append(task)
        current += 1
        if current % 10 == 0:
            await asyncio.wait(tasks)
            tasks = []
    if tasks:
        await asyncio.wait(tasks)


async def collect_hello_project_all_concert(start, end):
    tasks = []
    current = 0
    for page in range(start, end):
        url = PREFIX + '/event/?p={}'.format(page)
        task = asyncio.create_task(collect_news(url))
        tasks.append(task)
        current += 1
        if current % 10 == 0:
            await asyncio.wait(tasks)
            tasks = []
    if tasks:
        await asyncio.wait(tasks)


def run_collect_hello_project_news():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(collect_hello_project_all_news(1, 2))
    loop.run_until_complete(collect_hello_project_all_concert(1, 2))


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(collect_news('http://www.helloproject.com/news/'))
    # loop.run_until_complete(collect_hello_project_all_news(1, 101))
    run_collect_hello_project_news()