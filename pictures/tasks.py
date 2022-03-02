from django.core.mail import send_mail

from celery import shared_task

from pictures.service.recognize import recognize_multi
from hellofamilyclub.utils.websocket import send_message


@shared_task()
def send_recognize_mail(subject, message, from_email, recipient_list, fail_silently=False):
    send_mail(subject, message, from_email, recipient_list, fail_silently=fail_silently)


@shared_task()
def recognize_picture(user_id, picture_name):
    picture = mongo_db['images'].find_one({'name': picture_name})
    if not picture:
        send_message(user_id, '未找到图片', from_user='admin')
    else:
        recognize_multi(picture, picture['url'], 'BASE64', save=True, redownload=True)
        send_message(user_id, '成功更新人脸信息', from_user='admin')


if __name__ == '__main__':
    pass
