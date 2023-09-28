from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from event.models import *

class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ['id', 'created_at', 'updated_at', 'starttime', 'finishtime']

class MainEventSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    times = TimeSerializer(many=True, read_only = True)
    category = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model=Event
        fields=['id','day','times', 'college', 'category' ,'name','number','created_at','updated_at']
