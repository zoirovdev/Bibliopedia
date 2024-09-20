from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.BookListAPIView.as_view()),
    path('detail/<int:pk>', views.BookDetailAPIView.as_view()),
    path('search/', views.BookSearchAPIView.as_view())
]
