from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from event.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','nickname')

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    booth = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id','booth','user','content','created_at','updated_at']
    
    def get_booth(self, obj):
        return obj.event.id 


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ('day', 'date')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')

class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ['id', 'created_at', 'updated_at', 'starttime', 'finishtime']

class MenuSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ('id', 'menu', 'price', 'is_soldout', 'is_liked')

    def get_is_liked(self, obj):
        # 현재 요청을 보낸 사용자가 이벤트를 좋아요했는지 여부를 확인
        user = self.context['request'].user
        return user in obj.like.all()
    
class MenupatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'menu', 'price', 'is_soldout')


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('id','created_at', 'updated_at', 'content')

class DetailSerializer(serializers.ModelSerializer):
    day = DaySerializer(many=True)
    images = ImageSerializer(many=True)
    menus = MenuSerializer(many=True)
    comments = CommentSerializer(many=True)
    notices = NoticeSerializer(many=True)
    times = TimeSerializer(many=True)
    is_liked = serializers.SerializerMethodField()
    is_like_count = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'user',
            'day',
            'times',
            'college',
            'category',
            'name',
            'number',
            'thumnail',
            'opened',
            'busy',
            'began',
            'wheelchair',
            'is_show',
            'contact',
            'notices',
            'hashtag',
            'description',
            'images',
            'menus',
            'is_liked',
            'is_like_count',
            'created_at',
            'updated_at',
            'comments',
        ]

    def get_is_liked(self, obj):
        # 현재 요청을 보낸 사용자가 이벤트를 좋아요했는지 여부를 확인
        user = self.context['request'].user
        return user in obj.like.all()
    
    def get_is_like_count(self, obj): #좋아요 개수 
        return obj.like.count()
    


