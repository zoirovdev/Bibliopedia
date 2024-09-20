from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import User
from .serializers import MakeAdminSerializer, LoginSerializer, RegisterSerializer

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer

from drf_spectacular.utils import extend_schema


class UserList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=RegisterSerializer)
    def get(self, request):
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=
            { 
            'application/json': RegisterSerializer, 
            'multipart/form-data': RegisterSerializer  
            },
        responses=RegisterSerializer
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = serializer.instance
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=
            { 
            'application/json': LoginSerializer, 
            'multipart/form-data': LoginSerializer  
            },
        responses=RegisterSerializer
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=RegisterSerializer)
    def get(self, request, pk=None):
        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = request.user
        serializer = RegisterSerializer(user)
        return Response(serializer.data)


class LogoutAPIView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a RefreshToken object
            token = RefreshToken(refresh_token)

            # Blacklist the token
            token.blacklist()

            return Response({'detail': 'Logout successful.'}, status=status.HTTP_205_RESET_CONTENT)

        except (TokenError, InvalidToken) as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MakeAdminAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = MakeAdminSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'email'  # Assume email is the unique field to look up users by

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        """
        Override to find the user by email (or any unique identifier).
        """
        email = self.kwargs.get('email')
        return self.get_queryset().filter(email=email).first()
