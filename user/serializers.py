from rest_framework import serializers

from .models import HelloUser


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = HelloUser
        fields = ('id', 'username', 'nickname', 'email', 'phone', 'avatar', 'birthday')
