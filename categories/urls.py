from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.CategoryListAPIView.as_view()),
    path('detail/<int:pk>', views.CategoryDetailAPIView.as_view())
]
