from django.urls import path

from api.views import GetUpdateDeleteMessageAPIView, ListCreateMessageAPIView

urlpatterns = [
    path('messages', ListCreateMessageAPIView.as_view()),
    path('messages/<int:id>', GetUpdateDeleteMessageAPIView.as_view()),
]
