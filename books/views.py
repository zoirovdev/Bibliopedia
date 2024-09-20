from .models import Book
from .serializers import BookSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


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
    

class BookSearchAPIView(APIView):
    @extend_schema(
        summary="Search books with full-text search, filter by author or category",
        parameters=[
            OpenApiParameter(
                name='q',
                type=OpenApiTypes.STR,
                description="Search query for full-text search across book title and definition",
                required=False
            ),
            OpenApiParameter(
                name='author',
                type=OpenApiTypes.STR,
                description="Filter by author's name",
                required=False
            ),
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.STR,
                description="Filter by category name",
                required=False
            ),
        ],
        responses={200: BookSerializer(many=True)},
        description=(
            "Searches books based on the provided query. "
            "You can also filter results by author or category. "
            "The search looks through book titles and definitions using PostgreSQL's full-text search, "
            "and ranks the results by relevance."
        ),
    )
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)  
        author_name = request.query_params.get('author', None) 
        category_name = request.query_params.get('category', None)  
        
        books = Book.objects.all()
        
        if query:
            search_vector = SearchVector('title', weight='A') + SearchVector('definition', weight='B')
            search_query = SearchQuery(query)
            books = books.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.1)
        
        if author_name:
            books = books.filter(authors__full_name__icontains=author_name)
        
        if category_name:
            books = books.filter(categories__name__icontains=category_name)
        
        if query:
            books = books.order_by('-rank')
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        
        return Response(data={}, status=HTTP_200_OK)
