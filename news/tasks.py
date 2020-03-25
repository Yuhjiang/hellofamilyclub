import os

import django

from celery import shared_task
from bs4 import BeautifulSoup

profile = os.environ.get('HELLOFAMILYCLUB', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'hellofamilyclub.settings.{}'.format(profile))
django.setup()

from news.models import HelloNews, NewsType
from pictures.models import Group, Member

DEFAULT_GROUP = Group.objects.get(name_en='helloproject')
DEFAULT_MEMBER = Member.objects.get(name_en='DEFAULT')
DEFAULT_CATEGORY = NewsType.objects.get(name='EVENT')


@shared_task()
def get_information_from_page_task(html, url, category=None):
    try:
        get_information_from_page(html, url, category)
    except Exception as e:
        print('error, {}, url: {}'.format(e, url))


def get_information_from_page(html, url, category=None):
    detail_soup = BeautifulSoup(html, 'lxml')
    news_detail = get_news_detail_content(detail_soup)

    category = get_category(news_detail, category)
    title = get_title(news_detail).get_text()
    created_date = get_start_date(news_detail)
    groups = get_groups(news_detail)
    source = url
    members = get_members(news_detail)
    content = get_news_content(news_detail)
    if not HelloNews.objects.filter(source=url).exists():
        news = HelloNews.objects.create(title=title, content=content, created_date=created_date,
                                        source=source, category=category)
        news.group.set(groups)
        news.member.set(members)
        news.save()


def get_news_content(soup):
    content = str(soup.find(id='news_detail_contents'))
    return content


def get_members(soup):
    # 目前无法获取到成员
    return [DEFAULT_MEMBER]


def get_title(soup):
    return soup.find('h2')


def find_group_list(name_list):
    return Group.objects.filter(name_en__in=name_list)


def find_news_type(name):
    try:
        category = NewsType.objects.get(name=name)
    except NewsType.DoesNotExist:
        category = DEFAULT_CATEGORY
    return category


def get_news_detail_content(soup):
    news_detail = soup.find(id='news_detail')
    return news_detail


def get_start_date(soup):
    date = soup.find('time').string
    if '～' in date:
        result_date = date.split('～')[0]
    else:
        result_date = date
    result_date = '-'.join(result_date.split('/'))
    return result_date


def get_groups(soup):
    groups = []
    group_names = soup.select('.icon-name')
    for group in group_names:
        groups.append(group.attrs['class'][-1])
    if not groups:
        return [DEFAULT_GROUP]

    groups_object = find_group_list(groups)
    return groups_object


def get_category(soup, category=None):
    if not category:
        category = soup.select('.icon-schedule')
    if category:
        category = category[0].string
    else:
        category = DEFAULT_CATEGORY
    category = find_news_type(category)
    return category


if __name__ == '__main__':
    get_information_from_page(open('service/index.html'), 'http://www.helloproject.com/event/detail/8c67fe47d0252a98804812bc7570896f26eec1cf')
