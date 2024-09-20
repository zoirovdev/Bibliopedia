from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .models import Category
from .serializers import CategorySerializer

class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        request=
            { 
            'application/json': CategorySerializer, 
            'multipart/form-data': CategorySerializer  
            },
        responses=CategorySerializer
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=HTTP_201_CREATED)
    
    @extend_schema(
        responses=CategorySerializer
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)
    
    @extend_schema(
        responses=CategorySerializer
    )
    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)


