from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task, Change


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'password')
        model = User

    def validate_password(self, value: str) -> str:
        return make_password(value)


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Task

    def validate(self, attrs):
        date_string = self._kwargs.get('data').get('completed')
        if date_string:
            date = datetime.strptime(date_string, '%Y-%m-%d')
            if date < date.today():
                raise serializers.ValidationError(
                    'The date cannot be in the past!'
                )
        return attrs


class ChangeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('field_name', 'old_value', 'new_value', 'pub_date')
        model = Change
