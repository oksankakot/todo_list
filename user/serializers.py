from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        if not data.get("first_name"):
            raise serializers.ValidationError({"first_name": "This field is required."})
        if not data.get("username"):
            raise serializers.ValidationError({"username": "This field is required."})
        if not data.get("password"):
            raise serializers.ValidationError({"password": "This field is required."})
        return data
