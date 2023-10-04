from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, login
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .pagination import PaginationHandlerMixin
from .models import *
from .serializers import *
from event.models import *
import uuid
import math
from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr
from django.db.models import Q
#from event.serializers import *
# Create your views here.


class ProfileView(views.APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = get_object_or_404(User, pk=user.id)
        
        try:
            event = Event.objects.get(user=user)
            event_id = event.id
        except Event.DoesNotExist:
            event_id = None

        serializer = self.serializer_class(data)
        newdict=serializer.data
        newdict.update({'event_id':event_id})

        return Response({'message': "프로필 조회 성공", 'data': newdict}, status=HTTP_200_OK)

class EventPagination(PageNumberPagination):
    page_size = 10

'''
class LikedBoothListView(views.APIView, PaginationHandlerMixin):
    pagination_class = EventPagination
    serializer_class = BoothListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        day = request.GET.get('day')
        college = request.GET.get('college')
        category=request.GET.get('category')

        # 사용자가 "좋아요"한 부스 필터링
        liked_booths = Booth.objects.filter(like=user.id , is_show=False)

        # "day" 및 "college" 및 "category" 값이 있는 경우 필터링
        if day:
            liked_booths = liked_booths.filter(day=day)
        if college:
            liked_booths = liked_booths.filter(college=college)
        if category:
            liked_booths = liked_booths.filter(category=category)

        total = liked_booths.count()
        total_page = math.ceil(total / self.pagination_class.page_size)

        # 페이지네이션 적용
        liked_booths = self.paginate_queryset(liked_booths)

        serializer = self.serializer_class(liked_booths, many=True)

        return Response({'message': "좋아요한 부스 목록 조회 성공", 'total': total, 'total_page': total_page, 'data': serializer.data}, status=HTTP_200_OK)
'''

class LikedBoothListView(views.APIView, PaginationHandlerMixin):
    pagination_class = EventPagination
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        boothss = Event.objects.filter(like=user.id, is_show=False)
        day = request.GET.get('day')
        college = request.GET.get('college')
        category = request.GET.get('category')

        params = {'day': day, 'college': college, 'category' : category}
        arguments = {}
        for key, value in params.items():
            if value:
                arguments[key] = value

        booths = boothss.filter(**arguments).annotate(
                    number_order = Cast(Substr("number", 2), IntegerField())
                ).order_by("number_order")
        total = booths.__len__()
        total_page = math.ceil(total/10)
        booths = self.paginate_queryset(booths)

        if user:
            for booth in booths:
                if booth.like.filter(pk=user.id).exists():
                    booth.is_liked=True
        
        serializer = self.serializer_class(booths, many=True)
        return Response({'message': '좋아요한 부스 목록 조회 성공', 'total': total, 'total_page' : total_page, 'data': serializer.data}, status=HTTP_200_OK)


#좋아요한 메뉴 목록 조회. 필터링
'''
class LikedMenuListView(views.APIView, PaginationHandlerMixin):
    pagination_class = EventPagination
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        day = request.GET.get('day')
        college = request.GET.get('college')
        category=request.GET.get('category')

        # 사용자가 "좋아요"한 메뉴 필터링
        liked_menus = Menu.objects.filter(like=user.id)

        # "day" 및 "college" 값이 있는 경우 필터링
        if day:
            liked_menus = liked_menus.filter(day=day)
        if college:
            liked_menus = liked_menus.filter(college=college)
        if category:
            liked_menus = liked_menus.filter(category=category)
            

        total = liked_menus.count()
        total_page = math.ceil(total / self.pagination_class.page_size)

        # 페이지네이션 적용  
        liked_menus = self.paginate_queryset(liked_menus)

        serializer = self.serializer_class(liked_menus, many=True)

        return Response({'message': "좋아요한 메뉴 목록 조회 성공", 'total': total, 'total_page': total_page, 'data': serializer.data}, status=HTTP_200_OK)

class LikedMenuListView(views.APIView, PaginationHandlerMixin):
    pagination_class = EventPagination
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        menus = Menu.objects.filter(like=user.id)
        day = request.GET.get('day')
        college = request.GET.get('college')
        category = request.GET.get('category')

        params = {'day': day, 'college': college, 'category' : category}
        arguments = {}
        for key, value in params.items():
            if value:
                arguments[key] = value

        menus = Menu.objects.filter(**arguments).annotate(
                    number_order = Cast(Substr("number", 2), IntegerField())
                ).order_by("number_order")
        total = menus.__len__()
        total_page = math.ceil(total/10)
        menus = self.paginate_queryset(menus)

        if user:
            for menu in menus:
                if menu.like.filter(pk=user.id).exists():
                    menu.is_liked=True
        
        serializer = self.serializer_class(menus, many=True)
        return Response({'message': '좋아요한 메뉴 목록 조회 성공', 'total': total, 'total_page' : total_page, 'data': serializer.data}, status=HTTP_200_OK)

class LikedMenuListView(views.APIView, PaginationHandlerMixin):
    pagination_class = EventPagination
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        day = request.GET.get('day')
        college = request.GET.get('college')
        category = request.GET.get('category')

        params = {'day': day, 'college': college, 'category': category}
        arguments = Q(like=user.id)  

        for key, value in params.items():
            if value:
                arguments &= Q(**{key: value})  

        menus = Menu.objects.filter(arguments).annotate(
            number_order=Cast(Substr("number", 2), IntegerField())
        ).order_by("number_order")

        total = menus.count()
        total_page = math.ceil(total / 10)
        menus = self.paginate_queryset(menus)

        if user:
            for menu in menus:
                if menu.like.filter(pk=user.id).exists():
                    menu.is_liked = True

        serializer = self.serializer_class(menus, many=True)
        return Response({'message': '좋아요한 메뉴 목록 조회 성공', 'total': total, 'total_page': total_page, 'data': serializer.data}, status=HTTP_200_OK)
'''
class LikedMenuListView(views.APIView, PaginationHandlerMixin):
    pagination_class = EventPagination
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        menuss = Menu.objects.filter(like=user.id)
        day = request.GET.get('day')
        college = request.GET.get('college')
        category = request.GET.get('category')

        params = {'day': day, 'college': college, 'category' : category}
        arguments = {}
        for key, value in params.items():
            if value:
                arguments[key] = value

        menus = menuss.filter(**arguments)
        total = menus.__len__()
        total_page = math.ceil(total/10)
        menus = self.paginate_queryset(menus)

        if user:
            for menu in menus:
                if menu.like.filter(pk=user.id).exists():
                    menu.is_liked=True
        
        serializer = self.serializer_class(menus, many=True)
        return Response({'message': '좋아요한 메뉴 목록 조회 성공', 'total': total, 'total_page' : total_page, 'data': serializer.data}, status=HTTP_200_OK)

#좋아요한 공연 목록 조회. 필터링
'''
class LikedShowListView(views.APIView, PaginationHandlerMixin):
    pagination_class = EventPagination
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        day = request.GET.get('day')
        college = request.GET.get('college')
        category=request.GET.get('category')

        # 사용자가 "좋아요"한 공연 필터링
        liked_shows = Event.objects.filter(like=user.id , is_show = False)

        # "day" 및 "college" 값이 있는 경우 필터링
        if day:
            liked_shows = liked_shows.filter(day=day)
        if college:
            liked_shows = liked_shows.filter(college=college)
        if category:
            liked_shows = liked_shows.filter(category=category)

        total = liked_shows.count()
        total_page = math.ceil(total / self.pagination_class.page_size)

        # 페이지네이션 적용
        liked_shows = self.paginate_queryset(liked_shows)

        serializer = self.serializer_class(liked_shows, many=True)

        return Response({'message': "좋아요한 공연 목록 조회 성공", 'total': total, 'total_page': total_page, 'data': serializer.data}, status=HTTP_200_OK)

class LikedShowListView(views.APIView, PaginationHandlerMixin):
    pagination_class = EventPagination
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        shows = Event.objects.filter(like=user.id, is_show=True)
        day = request.GET.get('day')
        college = request.GET.get('college')
        category = request.GET.get('category')

        params = {'day': day, 'college': college, 'category' : category}
        arguments = {}
        for key, value in params.items():
            if value:
                arguments[key] = value

        shows = Event.objects.filter(**arguments).annotate(
                    number_order = Cast(Substr("number", 2), IntegerField())
                ).order_by("number_order")
        total = shows.__len__()
        total_page = math.ceil(total/10)
        shows = self.paginate_queryset(shows)

        if user:
            for show in shows:
                if show.like.filter(pk=user.id).exists():
                    show.is_liked=True
        
        serializer = self.serializer_class(shows, many=True)
        return Response({'message': '좋아요한 공연 목록 조회 성공', 'total': total, 'total_page' : total_page, 'data': serializer.data}, status=HTTP_200_OK)
'''
class LikedShowListView(views.APIView, PaginationHandlerMixin):
    pagination_class = EventPagination
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        showss = Event.objects.filter(like=user.id, is_show=True)
        day = request.GET.get('day')
        college = request.GET.get('college')
        category = request.GET.get('category')

        params = {'day': day, 'college': college, 'category' : category}
        arguments = {}
        for key, value in params.items():
            if value:
                arguments[key] = value

        shows = showss.filter(**arguments).annotate(
                    number_order = Cast(Substr("number", 2), IntegerField())
                ).order_by("number_order")
        total = shows.__len__()
        total_page = math.ceil(total/10)
        shows = self.paginate_queryset(shows)

        if user:
            for show in shows:
                if show.like.filter(pk=user.id).exists():
                    show.is_liked=True
        
        serializer = self.serializer_class(shows, many=True)
        return Response({'message': '좋아요한 공연 목록 조회 성공', 'total': total, 'total_page' : total_page, 'data': serializer.data}, status=HTTP_200_OK)
