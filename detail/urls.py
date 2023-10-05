from. views import *
from django.urls import path, include

app_name = "detail"

urlpatterns = [
    path("<int:pk>/", EventDetailView.as_view()),
    path("<int:event_id>/likes",EventLikeView.as_view()),
    path("menu/<int:menu_id>/likes",MenuLikeViewv.as_view()),
]