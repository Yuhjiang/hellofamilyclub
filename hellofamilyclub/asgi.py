import os
import django

from channels.routing import ProtocolTypeRouter

profile = os.environ.get('HELLOFAMILYCLUB', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'hellofamilyclub.settings.{}'.format(profile))
django.setup()

application = ProtocolTypeRouter({

})
