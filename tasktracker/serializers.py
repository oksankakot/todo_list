from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "user"]
        read_only_fields = ["user"]

    def validate(self, data):
        if not data.get("title"):
            raise serializers.ValidationError({"title": "This field is required."})
        if not data.get("status"):
            raise serializers.ValidationError({"status": "This field is required."})
        return data
