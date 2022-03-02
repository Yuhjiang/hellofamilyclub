from typing import List

from django.conf import settings

from pictures.models import Group, Member
from pictures.service.group_profile import GroupProfileCrawler
from pictures.utils import add_face_for_member


class HelloProfileRegister(object):
    """
    批量获取组合和成员，并添加到数据库
    """

    def __init__(self):
        self.crawler = GroupProfileCrawler(proxies=settings.REQUESTS_PROXY)
        self.groups: List[Group] = []
        self.members: List[Member] = []

    def save_to_database(self):
        self.crawler.fetch_groups()
        for g in self.crawler.group_list:
            try:
                grp = Group.objects.get(name_en=g.name_en)
                grp.favicon = g.favicon
                grp.save()
            except Group.DoesNotExist:
                grp = Group.objects.create(name=g.name_jp, name_en=g.name_en,
                                           name_jp=g.name_jp, color='#FFFFFF',
                                           homepage=g.url, favicon=g.favicon)
            self.groups.append(grp)
            members = self.crawler.fetch_members_from_group(g)
            for m in members:
                try:
                    member = Member.objects.get(name_en=m.name_en)
                    member.favicon = m.img_url
                    member.save(update_fields=['favicon'])
                except Member.DoesNotExist:
                    member = Member.objects.create(
                        name=m.name_jp, name_en=m.name_en, name_jp=m.name_jp,
                        birthday=m.birthday, hometown='', nickname=''
                    )
                    member.group.add(grp)
                self.members.append(member)

    def add_faces(self):
        for member in self.members:
            add_face_for_member(member.favicon, member)
