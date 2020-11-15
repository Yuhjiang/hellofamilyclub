from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer


def send_message(room_name, message, from_user):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notification_{}'.format(room_name),
        {
            'type': 'notification',
            'message': message,
            'from': from_user,
        }
    )
