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


class ChangeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('field_name', 'old_value', 'new_value', 'pub_date')
        model = Change
