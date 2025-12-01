import pytest
from rest_framework import status

from education.models import Course


def test_list_courses_success(auth_client, course):
    resp = auth_client.get("/api/v1/education/courses/")
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) >= 1
    assert "lessons_count" in resp.data[0]


def test_list_courses_unauth(api_client):
    resp = api_client.get("/api/v1/education/courses/")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED



def test_create_course_success(auth_client):
    payload = {"title": "New course", "description": "Some desc"}
    resp = auth_client.post("/api/v1/education/courses/", payload, format="json")
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.data["title"] == "New course"


def test_create_course_bad_data(auth_client):
    payload = {"description": "No title"}
    resp = auth_client.post("/api/v1/education/courses/", payload, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST



def test_retrieve_course_success(auth_client, course):
    resp = auth_client.get(f"/api/v1/education/courses/{course.id}/")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["id"] == course.id


def test_retrieve_course_not_found(auth_client):
    resp = auth_client.get("/api/v1/education/courses/99999/")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_update_course_owner_success(auth_client, course):
    payload = {"title": "Updated", "description": "Updated desc"}
    resp = auth_client.put(
        f"/api/v1/education/courses/{course.id}/",
        payload,
        format="json",
    )
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["title"] == "Updated"


def test_update_course_not_owner(api_client, other_user, course):
    api_client.force_authenticate(user=other_user)
    payload = {"title": "Hack", "description": "Hack"}
    resp = api_client.put(
        f"/api/v1/education/courses/{course.id}/",
        payload,
        format="json",
    )
    assert resp.status_code == status.HTTP_403_FORBIDDEN



def test_delete_course_owner_success(auth_client, course):
    resp = auth_client.delete(f"/api/v1/education/courses/{course.id}/")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert not Course.objects.filter(id=course.id).exists()


def test_delete_course_not_owner(api_client, other_user, course):
    api_client.force_authenticate(user=other_user)
    resp = api_client.delete(f"/api/v1/education/courses/{course.id}/")
    assert resp.status_code == status.HTTP_403_FORBIDDEN



def test_activate_course_success(auth_client, course):
    course.is_active = False
    course.save()
    resp = auth_client.post(f"/api/v1/education/courses/{course.id}/activate/")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["is_active"] is True


def test_activate_course_already_active(auth_client, course):
    resp = auth_client.post(f"/api/v1/education/courses/{course.id}/activate/")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST



def test_deactivate_course_success(auth_client, course):
    resp = auth_client.post(f"/api/v1/education/courses/{course.id}/deactivate/")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["is_active"] is False


def test_deactivate_course_not_owner(api_client, other_user, course):
    api_client.force_authenticate(user=other_user)
    resp = api_client.post(f"/api/v1/education/courses/{course.id}/deactivate/")
    assert resp.status_code == status.HTTP_403_FORBIDDEN



def test_list_course_lessons_success(auth_client, course, lesson):
    resp = auth_client.get(f"/api/v1/education/courses/{course.id}/lessons/")
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 1


def test_list_course_lessons_unauth(api_client, course):
    resp = api_client.get(f"/api/v1/education/courses/{course.id}/lessons/")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
