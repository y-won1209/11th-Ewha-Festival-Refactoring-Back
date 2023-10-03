from django.db import models
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
# Create your models here.

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'is_booth', 'is_tf', 'is_show']

from rest_framework import serializers

from event.models import Event, Menu, Image, Comment



class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class EventListSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    is_liked = serializers.BooleanField(default=False)
    
    class Meta:
        model = Event
        fields = fields = ['id', 'user', 'day', 'college', 'name', 'number', 'thumnail', 'description', 'is_liked', 'created_at', 'updated_at']
        read_only_fields= ('thumnail', )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'booth', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields= ('booth', 'user', )


class EventDetailSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    menus = MenuSerializer(read_only=True, many=True)
    images = ImageSerializer(read_only=True, many=True)
    is_liked = serializers.BooleanField(default=False)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'user', 'day', 'college', 'name', 'number', 'thumnail', 'notice', 'description', 'images', 'menus', 'is_liked', 'created_at', 'updated_at', 'comments']