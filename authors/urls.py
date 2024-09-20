from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.AuthorListAPIView.as_view()),
    path('detail/<int:pk>', views.AuthorDetailAPIView.as_view())
]
