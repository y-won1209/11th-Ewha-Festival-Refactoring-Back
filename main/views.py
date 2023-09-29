from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from event.models import *
from .serializers import *
from django.db.models import OuterRef, Subquery, F, Max,ExpressionWrapper,IntegerField
from django.db.models.functions import Cast
from django.db.models import CharField


class EventStartTimeInt:
    def __init__(self, event, starttime_int):
        self.event = event  
        self.starttime_int = starttime_int  

class MainView(views.APIView):
    serializer_class = MainEventSerializer
    def get(self, request):
        location= request.GET.get('college')
        day= request.GET.get('day')
        all_shows = Event.objects.filter(is_show=True).all()
        if(location):
            all_shows=all_shows.filter(college=location)
        if(day):
            all_shows=all_shows.filter(day=day)
            # 공연 날짜 인덱스
            num=int(day)-1

            # 해당 날짜의 시작시간+공연 담을 리스트
            all_show_objects = []  

            for show in all_shows:
                day_time = Time.objects.filter(event=show).order_by('id')[num].starttime
                starttime_split = day_time.split(':')
                starttime_int = int(starttime_split[0]) * 60 + int(starttime_split[1])
                show_time = EventStartTimeInt(show, starttime_int)
                all_show_objects.append(show_time)

            # starttimeInt 기준 정렬
            all_show_objects = sorted(all_show_objects, key=lambda x: x.starttime_int)

            # 다시 Event 객체로 저장
            serialized_shows = []
            for show_obj in all_show_objects:
                show_instance = show_obj.event  
                serializer = self.serializer_class(show_instance)
                serialized_show = serializer.data 
                serialized_shows.append(serialized_show)

        
            return Response({'message':'공연 일정표 조회 성공', 'data': serialized_shows}, status=status.HTTP_200_OK)
        else:
            eventserializer=self.serializer_class(all_shows,many=True)
            return Response({'message':'공연 일정표 조회 성공', 'data': eventserializer.data}, status=status.HTTP_200_OK)