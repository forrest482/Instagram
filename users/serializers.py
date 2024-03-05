from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'is_private', 'bio', 'profile_picture',
                  'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        instance = super(UserProfileSerializer, self).update(
            instance, validated_data)

        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
