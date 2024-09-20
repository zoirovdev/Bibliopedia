from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.QuoteListAPIView.as_view()),
    path('detail/<int:pk>', views.QuoteDetailAPIView.as_view())
]
