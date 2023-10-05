from rest_framework import serializers

from .models import *
from accounts.models import User


class EventListSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    is_liked = serializers.BooleanField(default=False)
    is_like_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'user', 'day', 'college', 'category', 'name', 'number', 'thumnail', 'opened', 'hashtag', 'description', 'is_liked', 'is_like_count', 'busy', 'began', 'wheelchair', 'is_show', 'contact', 'created_at', 'updated_at']
        read_only_fields= ('thumnail', )

    def get_is_like_count(self, obj):
        return obj.like.count()



