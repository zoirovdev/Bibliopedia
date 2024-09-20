from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.LanguageListAPIView.as_view()),
    path('detail/<int:pk>', views.LanguageDetailAPIView.as_view())
]
