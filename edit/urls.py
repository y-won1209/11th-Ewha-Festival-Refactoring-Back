from. views import *
from django.urls import path, include

app_name = "edit"

urlpatterns = [
    path("<int:pk>/", EventDetailView.as_view()),
    path("<int:pk>/menus/", MenuListView.as_view()),
    path('<int:pk>/menus/<int:menu_pk>/', MenuDetailView.as_view()),
]
