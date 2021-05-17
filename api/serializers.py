from rest_framework import serializers

from api.models import Message


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    views = serializers.IntegerField(required=False, read_only=True)
    created_at = serializers.DateTimeField("%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField("%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'views', 'created_at', 'updated_at']
