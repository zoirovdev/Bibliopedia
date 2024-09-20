from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.LanguageAPIView.as_view()),
    path('detail/<int:pk>', views.LanguageAPIView.as_view())
]
