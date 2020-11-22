from typing import List, Dict

from django.core.mail import send_mail
from celery import shared_task

from pictures.service.recognize import recognize_multi
from pictures.service.config import mongo_db
from utils.websocket import send_message


@shared_task()
def send_recognize_mail(subject, message, from_email, recipient_list, fail_silently=False):
    send_mail(subject, message, from_email, recipient_list, fail_silently=fail_silently)


@shared_task()
def recognize_picture(user_id, picture_name):
    picture = mongo_db['images'].find_one({'name': picture_name})
    if not picture:
        send_message(user_id, '未找到图片', from_user='admin')
    else:
        members = recognize_multi(picture, picture['url'], 'BASE64', save=True,
                                  redownload=True)
        message = member_from_picture(members)
        send_message(user_id, message, from_user='admin')


def member_from_picture(members: List[Dict]) -> str:
    """
    将人脸识别得到的成员，组合成weboscket可以推送的信息
    :param members: [
    {'id': 16, 'name_en': 'ayano_kawamura', 'name_jp': '川村文乃',
     'group': 'angerme'}]
    :return: 成员有: 川村文乃
    """
    names = [m['name_jp'] for m in members]
    return '成功更新人脸信息，成员有:{}'.format(', '.join(names))


if __name__ == '__main__':
    pass
