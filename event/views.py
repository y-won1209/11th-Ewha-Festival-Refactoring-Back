#import boto3
#import uuid
import math

from django.shortcuts import get_object_or_404
from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr
from django.http import HttpResponseBadRequest
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *

#from .storages import FileUpload, s3_client


class EventListView(views.APIView):
    serializer_class = EventListSerializer

    def get(self, request):
        user = request.user
        #필터링 -> day, college, category
        day = request.GET.get('day')
        college = request.GET.get('college')
        category = request.GET.get('category')
        type=request.GET.get('type')
       
       # is_show 값을 기반으로 type 값을 설정
        # is_show = request.GET.get('is_show')
        events = Event.objects.all()
        # if is_show is not None:
        #     is_show = is_show.lower() == 'true'  # 문자열 'true'를 True로 변환
        #     if is_show:
        #         events = events.filter(type = 2)
        #     else:
        #         events = events.filter(type = 1)
        if type:
            if(type=='2'):
                #is_show = is_show.lower() == 'true'  # 문자열 'true'를 True로 변환
                events = events.filter(is_show = True)
            elif (type=='1'):
                events = events.filter(is_show = False)

        params = {'day': day, 'college': college, 'category': category}
        arguments = {}
        for key, value in params.items():
            if value:
                arguments[key] = value
        if arguments:
            events = events.filter(**arguments).annotate(
                    number_order = Cast(Substr("number", 2), IntegerField())
                ).order_by("number_order")

        if user:
            for event in events:
                if event.like.filter(pk=user.id).exists():
                    event.is_liked=True
        
        serializer = self.serializer_class(events, many=True)
        return Response({'message': '부스/공연 목록 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)

class SearchView(views.APIView):
    serializer_class = EventListSerializer

    def get(self, request):
        user = request.user
        keyword = request.GET.get('keyword', )  # 기본값으로 빈 문자열을 할당합니다.

        events = (Event.objects.filter(name__icontains=keyword) | Event.objects.filter(menus__menu__contains=keyword)).distinct()

        if user:
            for event in events:
                if event.like.filter(pk=user.id).exists():
                    event.is_liked = True

        serializer = self.serializer_class(events, many=True)

        return Response({'message': '부스/공연 검색 성공', 'data': serializer.data}, status=HTTP_200_OK)
