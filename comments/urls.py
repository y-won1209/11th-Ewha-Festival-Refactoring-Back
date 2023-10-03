from django.urls import path
from .views import *

app_name = 'comments'

urlpatterns = [
    path('<int:pk>/', CommentView.as_view()),
    path('<int:pk>/del/<int:comment_pk>/', CommentView.as_view()),

]