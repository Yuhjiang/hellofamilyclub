from django.core.management.base import BaseCommand
from django.utils import timezone
from pymongo import MongoClient

from pictures.models import Member, Picture


class Command(BaseCommand):
    help = '迁移mongodb上的识别结果到mysql'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        members = list(Member.objects.filter().only('id', 'name_jp'))
        self.member_dict = {m.name_jp: m.id for m in members}

    def handle(self, *args, **options):
        self.modify_time()

    def get_member(self, name_jp: str):
        return self.member_dict.get(name_jp)

    def migrate(self):
        client = MongoClient('mongodb://10.20.3.232:27017/')
        db = client['hellofamily']
        for i in db['images'].find():
            name = i['name']
            try:
                pic = Picture.objects.get(pic_id=name.split('.')[0])
            except Picture.DoesNotExist:
                pic = Picture.objects.create(
                    pic_id=name.split('.')[0],
                    name=name,
                    url=i['url'],
                    create_time=i['created_time'],
                    create_date=i['created_date'],
                )
            member_ids = []
            for d in i['members']:
                id_ = self.get_member(d['name_jp'])
                if id_:
                    member_ids.append(id_)
            pic.set_members(member_ids)

    def modify_time(self, *args, **kwargs):
        client = MongoClient('mongodb://10.20.3.232:27017/')
        db = client['hellofamily']
        for i in db['images'].find():
            name = i['name']
            pic_id = name.split('.')[0]
            Picture.objects.filter(pic_id=pic_id).update(
                create_time=i['created_time'].astimezone(timezone.utc),
                create_date=i['created_date'],
            )
