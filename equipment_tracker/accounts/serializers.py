from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.core import exceptions as django_exceptions
from rest_framework import serializers
from accounts.models import CustomUser
from rest_framework.settings import api_settings
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_str
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from drf_extra_fields.fields import Base64ImageField

# There can be multiple subject instances with the same name, only differing in course, year level, and semester. We filter them here


class CustomUserSerializer(BaseUserSerializer):
    avatar = Base64ImageField()

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ('username', 'email', 'avatar', 'first_name', 'last_name',)


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password', 'placeholder': 'Password'})

    class Meta:
        model = CustomUser    # Use your custom user model here
        fields = ('username', 'email', 'password', 'avatar',
                  'first_name', 'last_name')

    def validate(self, attrs):
        user = self.Meta.model(**attrs)
        password = attrs.get("password")
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return super().validate(attrs)

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user
