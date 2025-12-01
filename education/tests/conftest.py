import pytest
from django.contrib.auth.models import get_user_model
from rest_framework.test import APIClient

from education.models import Course, Lesson

User = get_user_model()

def api_client():
    return APIClient()
def user(db):
    return User.objects.create_user(username='user1', password='pass12345')

def other_user(db):
    return User.obj
    ects.create_user(username='user2', password='pass12345')

def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

def course(user):
    return Course.objects.create(
        title='Test Course',
        description='A course for testing',
        owner=user
    )


def lesson(course):    
    return Lesson.objects.create(
    course=course,
    title='Test Lesson',
    content='Lesson content',
    order=1,
)
