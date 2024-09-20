from .models import Quote
from .serializers import QuoteSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from drf_spectacular.utils import extend_schema


class QuoteListAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    @extend_schema(
        request=
            { 
            'application/json': QuoteSerializer, 
            'multipart/form-data': QuoteSerializer  
            },
        responses=QuoteSerializer
    )
    def post(self, request):
        serializer = QuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=HTTP_201_CREATED)
    

    @extend_schema(
        responses=QuoteSerializer
    )
    def get(self, request):
        quotes = Quote.objects.order_by('?').all()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)

class QuoteDetailAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    @extend_schema(
        request=
            { 
            'application/json': QuoteSerializer, 
            'multipart/form-data': QuoteSerializer  
            },
        responses=QuoteSerializer
    )
    def put(self, request, pk):
        quote = Quote.objects.get(pk=pk)
        serializer = QuoteSerializer(quote, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=HTTP_200_OK)
    
    @extend_schema(
        responses=QuoteSerializer
    )
    def delete(self, request, pk):
        quote = Quote.objects.get(pk=pk)
        quote.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    