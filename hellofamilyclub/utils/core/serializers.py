from rest_framework import serializers


class BasicResponseSerializer(serializers.Serializer):
    error = serializers.IntegerField(label='错误码')
    detail = serializers.CharField(label='错误信息')

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
