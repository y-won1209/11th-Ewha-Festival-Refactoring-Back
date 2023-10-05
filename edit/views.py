from django.shortcuts import render, get_object_or_404
from rest_framework.status import HTTP_200_OK
from rest_framework import views
from rest_framework import status
from .models import *
from edit.serializers import *
from django.http import Http404


from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .permissions import IsAuthorOrReadOnly


from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr


from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *
from .permissions import IsAuthorOrReadOnly


# Create your views here.


class EventDetailView(views.APIView):
    serializer_class = DetailSerializer
    permission_classes = [IsAuthorOrReadOnly]
    
    def get_object(self, pk):
        event = get_object_or_404(Event, pk=pk)
        self.check_object_permissions(self.request, event)
        return event

    def patch(self, request, pk):
        event = self.get_object(pk=pk)
        serializer = self.serializer_class(data=request.data, instance=event, partial=True,context={'request':request})

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '이벤트 정보 수정 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '이벤트 정보 수정 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    


class MenuListView(views.APIView):
    serializer_class = MenuSerializer

    def get(self, request, pk):
        menus = Menu.objects.filter(event=pk)
        
        if menus.exists():
            serializer = self.serializer_class(menus, many=True, context={'request': request})
            return Response({'message': '메뉴 목록 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            raise Http404("찾을 수 없습니다.")
        
        
class MenuDetailView(views.APIView):
    serializer_class = MenupatchSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self, pk):
        event = get_object_or_404(Event, pk=pk)
        self.check_object_permissions(self.request, event)
        return event

    def patch(self, request, pk, menu_pk):
        event = self.get_object(pk=pk)
        menu = get_object_or_404(Menu, event=event, pk=menu_pk)

        serializer = self.serializer_class(data=request.data, instance=menu, partial=True,
                                context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '메뉴 정보 수정 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '메뉴 정보 수정 실패', 'data': serializer.errors},
                            status=HTTP_400_BAD_REQUEST)