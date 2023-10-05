from django.urls import path
from .views import *

app_name = 'event'

urlpatterns = [
    path('', EventListView.as_view()),
    path('search/', SearchView.as_view()),
]