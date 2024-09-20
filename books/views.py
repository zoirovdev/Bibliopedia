from .models import Book
from .serializers import BookSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

class BookListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=
            { 
            'application/json': BookSerializer, 
            'multipart/form-data': BookSerializer  
            },
        responses=BookSerializer
    )
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        responses=BookSerializer
    )
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)
    
class BookDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=
            { 
            'application/json': BookSerializer, 
            'multipart/form-data': BookSerializer  
            },
        responses=BookSerializer
    )
    def put(self, request, pk):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=HTTP_200_OK)
    
    @extend_schema(
        responses=BookSerializer
    )
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(data=serializer.data, status=HTTP_200_OK)
    
    @extend_schema(
        responses=BookSerializer
    )
    def delete(self, request, pk):
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response(status=HTTP_204_NO_CONTENT)