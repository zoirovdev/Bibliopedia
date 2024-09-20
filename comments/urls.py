from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.CommentListAPIView.as_view()),
    path('detail/<int:pk>', views.CommentDetailAPIView.as_view()),
    path('get-comments-by-book/<int:pk>', views.GetCommentsByBookAPIView.as_view())
]
