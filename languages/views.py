from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .models import Language
from .serializers import LanguageSerializer

class LanguageAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        request=
            { 
            'application/json': LanguageSerializer, 
            'multipart/form-data': LanguageSerializer  
            },
        responses=LanguageSerializer
    )
    def post(self, request):
        serializer = LanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=HTTP_201_CREATED)
    
    @extend_schema(
        responses=LanguageSerializer
    )
    def get(self, request):
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)
    
    @extend_schema(
        responses=LanguageSerializer
    )
    def delete(self, request, pk):
        language = Language.objects.get(pk=pk)
        language.delete()
        return Response(status=HTTP_204_NO_CONTENT)