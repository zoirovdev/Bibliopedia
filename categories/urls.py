from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.CategoryAPIView.as_view()),
    path('detail/', views.CategoryAPIView.as_view())
]
