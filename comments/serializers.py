from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from event.models import *
from accounts.models import *

class ComUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id','nickname']

class CommentSerializer(serializers.ModelSerializer):
    user = ComUserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'event', 'user', 'content','created_at','updated_at']
        read_only_fields= ('event', 'user' )