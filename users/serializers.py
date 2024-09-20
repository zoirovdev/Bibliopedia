from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password':{'write_only':True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)


class MakeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_staff', 'is_superuser']

    def update(self, instance, validated_data):
        """
        Update the user instance with admin privileges.
        """
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.save()
        return instance