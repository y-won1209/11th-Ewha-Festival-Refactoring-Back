from django.urls import path
from .views import *

app_name = 'mypage'

urlpatterns = [
    path('', ProfileView.as_view()),
    path('booth/likes/', LikedBoothListView.as_view()),
    path('menu/likes/', LikedMenuListView.as_view()),
    path('show/likes/', LikedShowListView.as_view()),
]