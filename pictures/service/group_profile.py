from datetime import date, datetime
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup


class GroupDO(object):
    def __init__(self, url: str, name_en: str, name_jp: str, favicon: str):
        self.url = url
        self.name_en = name_en
        self.name_jp = name_jp
        self.favicon = favicon

    def __repr__(self):
        return f'name_en: {self.name_en}, name_jp: {self.name_jp}, ' \
               f'url: {self.url}'


class MemberDO(object):
    def __init__(self, name_en: str, name_jp: str, img_url: str,
                 birthday: Optional[date], joined_time: Optional[date]):
        self.name_en = name_en
        self.name_jp = name_jp
        self.img_url = img_url
        self.birthday = birthday
        self.joined_time = joined_time

    def __repr__(self):
        return f'name_jp: {self.name_jp}, birthday: {self.birthday}, joined_time: {self.joined_time}'


class GroupProfileCrawler(object):
    """
    爬取hello!project官网的组合数据
    """

    def __init__(self, official_site: str = 'http://www.helloproject.com',
                 proxies=None):
        self.official_site = official_site
        self.artist_site = self.official_site + '/artist/'
        self.group_list: List[GroupDO] = []
        self.member_dict: Dict[str, List[MemberDO]] = {}
        self.proxies = proxies

    def fetch_groups(self):
        text = requests.get(self.artist_site, proxies=self.proxies).text
        soup = BeautifulSoup(text, 'html.parser')
        group_list = soup.find('nav', class_='artist_listbox').find_all('div')
        for g in group_list:
            self.parse_group(g)

    def parse_group(self, group_soup):
        name_en = group_soup.find('span').get('class')[0]
        name_jp = group_soup.find('span').text
        url = self.official_site + group_soup.find('a').get('href')
        favicon = group_soup.find('img').get('src')
        self.group_list.append(GroupDO(url, name_en, name_jp, favicon))

    def fetch_members_from_group(self, group: GroupDO) -> List[MemberDO]:
        members = []
        self.member_dict[group.name_en] = members
        profile_site = group.url + 'profile/'
        text = requests.get(profile_site, self.proxies).text
        member_list = BeautifulSoup(text, 'html.parser').find(
            id='profile_memberlist').find_all('li')
        for m in member_list:
            mem = self.parse_member(m)
            if mem.name_jp == '在籍者なし':
                continue
            members.append(mem)
        return members

    def parse_member(self, m) -> MemberDO:
        name_en = m.find('a').get('href').split('/')[-2]
        name_jp = m.find('h4').text
        if name_jp == '在籍者なし':
            return MemberDO(name_en, name_jp, '', None, None)
        img_url = m.find('img').get('src')
        birthday = m.find_all('dd')[0].text
        birthday = datetime.strptime(birthday, '%Y年%m月%d日').date()
        joined_time = self.parse_member_joined_date(m.find('a').get('href'))
        return MemberDO(name_en, name_jp, img_url, birthday, joined_time)

    def parse_member_joined_date(self, site) -> Optional[date]:
        """
        从成员的个人主页获取加入团队的日期
        :return:
        """
        site = self.official_site + site
        resp = requests.get(site, proxies=self.proxies)
        soup = BeautifulSoup(resp.text, 'html.parser')
        date_str = soup.find_all('dt', class_='question'
                                 )[-1].find_next().text.split('\u3000')[0]
        try:
            return datetime.strptime(date_str, '%Y年%m月%d日').date()
        except ValueError:
            return None


if __name__ == '__main__':
    crawler = GroupProfileCrawler(proxies={'http': 'http://localhost:1087'})
    crawler.fetch_groups()
    for grp in crawler.group_list:
        crawler.fetch_members_from_group(grp)
