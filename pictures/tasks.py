from django.core.mail import send_mail

from celery import shared_task


@shared_task()
def send_recognize_mail(subject, message, from_email, recipient_list, fail_silently=False):
    send_mail(subject, message, from_email, recipient_list, fail_silently=fail_silently)


if __name__ == '__main__':
    pass
