from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .models import Comment
from .serializers import CommentSerializer

class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=
            { 
            'application/json': CommentSerializer, 
            'multipart/form-data': CommentSerializer  
            },
        responses=CommentSerializer
    )
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=HTTP_201_CREATED)
    
class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=
            { 
            'application/json': CommentSerializer, 
            'multipart/form-data': CommentSerializer  
            },
        responses=CommentSerializer
    )
    def put(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=HTTP_200_OK)
    
class GetCommentsByBookAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        responses=CommentSerializer
    )
    def get(self, request, pk):
        comments = Comment.objects.filter(book=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)