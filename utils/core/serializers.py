from rest_framework import serializers


class BasicSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BasicResponseSerializer(BasicSerializer):
    count = serializers.IntegerField(label='总数')
    next = serializers.URLField()
    previous = serializers.URLField()
    results = serializers.CharField()