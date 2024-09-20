from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.QuoteAPIView.as_view()),
    path('detail/<int:pk>', views.QuoteAPIView.as_view())
]
