from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db.models import Count , Q
from rest_framework import serializers

from .models import Course, Lesson

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
class CourseSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'is_active', 'owner', 'created_at', 'updated_at','lessons_count']

        read_only_fields = ['id', 'is_active', 'created_at', 'updated_at','lessons_count', 'owner']

        def create(self, validated_data):
            validated_data['owner'] = self.context['request'].user
            return super().create(validated_data)
        
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'order', 'indentation', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at','order','indentation','course']

    

