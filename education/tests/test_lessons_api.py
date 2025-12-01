import pytest
from rest_framework import status

from education.models import Lesson


def test_create_lesson_success(auth_client, course):
    payload = {"title": "New lesson", "content": "Body"}
    url = f"/api/v1/education/lessons/?course_id={course.id}"
    resp = auth_client.post(url, payload, format="json")
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.data["title"] == "New lesson"


def test_create_lesson_missing_course(auth_client):
    payload = {"title": "New lesson", "content": "Body"}
    url = "/api/v1/education/lessons/"
    resp = auth_client.post(url, payload, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


def test_move_lesson_before_other_success(auth_client, course, lesson):
   
    l2 = Lesson.objects.create(
        course=course,
        title="L2",
        content="C2",
        order=2,
    )
    url = f"/api/v1/education/lessons/{l2.id}/move"
    resp = auth_client.put(url, {"before_lesson_id": lesson.id}, format="json")
    assert resp.status_code == status.HTTP_200_OK
   
    l2.refresh_from_db()
    lesson.refresh_from_db()
    assert l2.order <= lesson.order


def test_move_lesson_invalid_before_id(auth_client, lesson):
    url = f"/api/v1/education/lessons/{lesson.id}/move"
    resp = auth_client.put(url, {"before_lesson_id": 99999}, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


def test_delete_lesson_success(auth_client, lesson):
    url = f"/api/v1/education/lessons/{lesson.id}/"
    resp = auth_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert not Lesson.objects.filter(id=lesson.id).exists()


def test_delete_lesson_not_owner(api_client, other_user, lesson):
    api_client.force_authenticate(user=other_user)
    url = f"/api/v1/education/lessons/{lesson.id}/"
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN



def test_publish_lesson_success(auth_client, lesson):
    url = f"/api/v1/education/lessons/{lesson.id}/publish/"
    resp = auth_client.post(url)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["is_published"] is True


def test_publish_lesson_not_owner(api_client, other_user, lesson):
    api_client.force_authenticate(user=other_user)
    url = f"/api/v1/education/lessons/{lesson.id}/publish/"
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN



def test_unpublish_lesson_success(auth_client, lesson):
    lesson.is_published = True
    lesson.save()
    url = f"/api/v1/education/lessons/{lesson.id}/unpublish/"
    resp = auth_client.post(url)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["is_published"] is False


def test_unpublish_lesson_already_unpublished(auth_client, lesson):
    url = f"/api/v1/education/lessons/{lesson.id}/unpublish/"
    resp = auth_client.post(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
