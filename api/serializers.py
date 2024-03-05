import uuid
from datetime import datetime

from rest_framework import serializers

from api.models import User, NewsStory, Agency


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return value.strftime('%Y-%m-%d %H:%M:%S')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name')


class NewsStorySerializer(serializers.ModelSerializer):
    date = CustomDateTimeField(read_only=True)

    class Meta:
        model = NewsStory
        fields = ('id', 'key', 'author', 'headline', 'category', 'region', 'date', 'details',)

    def create(self, validated_data):
        unique_key = f'{uuid.uuid4().hex}_{int(datetime.utcnow().timestamp())}'
        truncated_key = unique_key[:20]
        validated_data['key'] = truncated_key
        return super().create(validated_data)


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ('id', 'agency_name', 'url', 'agency_code')
