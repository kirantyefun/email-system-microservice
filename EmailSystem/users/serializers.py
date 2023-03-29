from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.validators import ValidationError

UserModel = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self, validated_data):
        return UserModel.objects.create_user(
            email=validated_data['email'], username=validated_data['username'], password=validated_data['password'])


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        print(clean_data)
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise ValidationError('User not found')
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username')
