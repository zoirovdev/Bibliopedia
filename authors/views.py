from .models import Author
from .serializers import AuthorSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema


class AuthorListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = MultiPartParser, FormParser

    @extend_schema(
        request=
            { 
            'application/json': AuthorSerializer, 
            'multipart/form-data': AuthorSerializer  
            },
        responses=AuthorSerializer
    )
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=HTTP_201_CREATED)
    
    @extend_schema(
        responses=AuthorSerializer
    )
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)
    

class AuthorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=
            { 
            'application/json': AuthorSerializer, 
            'multipart/form-data': AuthorSerializer  
            },
        responses=AuthorSerializer
    )
    def put(self, request, pk):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=HTTP_200_OK)
    
    @extend_schema(
        responses=AuthorSerializer
    )
    def get(self, request, pk):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author)
        return Response(data=serializer.data, status=HTTP_200_OK)
    
    
    @extend_schema(
        responses=AuthorSerializer
    )
    def delete(self, request, pk):
        author = Author.objects.get(pk=pk)
        author.delete()
        return Response(status=HTTP_204_NO_CONTENT)