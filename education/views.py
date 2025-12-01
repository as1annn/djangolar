from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Course, Lesson
from .serializers import LessonSerializer
from drf_spectacular.utils import extend_schema



@extend_schema(tags=["Courses"])
class CourseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Course.objects.annotate(
            lessons_count=Count(
                "lessons",
                filter=Q(lessons__deleted_at__isnull=True),
            )
        )
        is_active_param = self.request.query_params.get("is_active")
        if is_active_param is not None:
            if is_active_param.lower() == "true":
                qs = qs.filter(is_active=True)
            elif is_active_param.lower() == "false":
                qs = qs.filter(is_active=False)
        return qs

    def get_object(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)

    @extend_schema(
        summary="List courses",
        description="List all courses. Optional filter: is_active=true/false",
        parameters=[
            OpenApiParameter(
                name="is_active",
                description="Filter by active status: true or false",
                required=False,
                type=OpenApiTypes.STR,
            )
        ],
        responses=CourseSerializer(many=True),
    )
    def list(self, request):
        courses = self.get_queryset()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a course",
        request=CourseSerializer,
        responses=CourseSerializer,
    )
    def create(self, request):
        serializer = CourseSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Retrieve a course",
        responses=CourseSerializer,
    )
    def retrieve(self, request, pk=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @extend_schema(
        summary="Update a course",
        request=CourseSerializer,
        responses=CourseSerializer,
    )
    def update(self, request, pk=None):
        course = self.get_object(pk)
        if course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(course, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete a course",
        responses={204: None},
    )
    def destroy(self, request, pk=None):
        course = self.get_object(pk)
        if course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Activate a course",
        responses=CourseSerializer,
    )
    @action(detail=True, methods=["post"], url_path="activate")
    def activate(self, request, pk=None):
        course = self.get_object(pk)
        if course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if course.is_active:
            return Response({"detail": "Course is already active."}, status=status.HTTP_400_BAD_REQUEST)

        course.is_active = True
        course.save(update_fields=["is_active"])
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @extend_schema(
        summary="Deactivate a course",
        responses=CourseSerializer,
    )
    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        course = self.get_object(pk)
        if course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not course.is_active:
            return Response({"detail": "Course is already inactive."}, status=status.HTTP_400_BAD_REQUEST)

        course.is_active = False
        course.save(update_fields=["is_active"])
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @extend_schema(
        summary="List lessons of a course",
        responses=LessonSerializer(many=True),
    )
    @action(detail=True, methods=["get"], url_path="lessons")
    def lessons(self, request, pk=None):
        course = self.get_object(pk)
        lessons = course.lessons.filter(deleted_at__isnull=True)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    

class LessonViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(
            Lesson.objects.select_related("course", "course__owner"),
            pk=pk,
        )

    @extend_schema(
        summary="Create a lesson",
        description="course_id, title, content",
        request=LessonSerializer,
        responses=LessonSerializer,
    )
    def create(self, request):
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"detail": "course_id is required"}, status=400)

        course = get_object_or_404(Course.objects.select_related("owner"), id=course_id)
        if course.owner != request.user:
            return Response(status=403)

        title = request.data.get("title")
        content = request.data.get("content")
        if not title or not content:
            return Response({"detail": "title and content required"}, status=400)

        with transaction.atomic():
            for lesson in course.lessons.filter(deleted_at__isnull=True):
                lesson.order = Decimal(lesson.order) + 1
                lesson.save(update_fields=["order"])

            lesson = Lesson.objects.create(
                course=course,
                title=title,
                content=content,
                order=Decimal(1),
                indentation=0,
            )

        return Response(LessonSerializer(lesson).data, status=201)

    @extend_schema(
        summary="Move a lesson",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "before_lesson_id": {"type": ["integer", "null"]},
                },
                "required": ["before_lesson_id"],
            }
        },
        responses={
            200: {
                "type": "object",
                "properties": {
                    "order": {"type": "number"},
                    "indentation": {"type": "integer"},
                },
            }
        },
    )
    @action(detail=True, methods=["put"], url_path="move")
    def move(self, request, pk=None):
        lesson = self.get_object(pk)
        course = lesson.course

        if course.owner != request.user:
            return Response(status=403)

        before_lesson_id = request.data.get("before_lesson_id")

        lessons = list(course.lessons.filter(deleted_at__isnull=True).order_by("order"))

        lessons = [l for l in lessons if l.id != lesson.id]

        if before_lesson_id is None:
            lessons.append(lesson)
            lesson.indentation = 0
        else:
            try:
                before_lesson_id = int(before_lesson_id)
            except:
                return Response({"detail": "Invalid before_lesson_id"}, status=400)

            target = next((l for l in lessons if l.id == before_lesson_id), None)
            if target is None:
                return Response({"detail": "before_lesson_id not found"}, status=400)

            index = lessons.index(target)
            lessons.insert(index, lesson)
            lesson.indentation = target.indentation

        with transaction.atomic():
            for i, l in enumerate(lessons, start=1):
                l.order = Decimal(i)
                l.save(update_fields=["order"])
            lesson.save(update_fields=["indentation"])

        return Response({"order": float(lesson.order), "indentation": lesson.indentation})

    @extend_schema(summary="Delete a lesson", responses={204: None})
    def destroy(self, request, pk=None):
        lesson = self.get_object(pk)
        if lesson.course.owner != request.user:
            return Response(status=403)
        lesson.delete()
        return Response(status=204)

    @extend_schema(summary="Publish a lesson", responses=LessonSerializer)
    @action(detail=True, methods=["post"], url_path="publish")
    def publish(self, request, pk=None):
        lesson = self.get_object(pk)
        if lesson.course.owner != request.user:
            return Response(status=403)
        if lesson.is_published:
            return Response({"detail": "already published"}, status=400)

        lesson.is_published = True
        lesson.save(update_fields=["is_published"])
        return Response(LessonSerializer(lesson).data)

    @extend_schema(summary="Unpublish a lesson", responses=LessonSerializer)
    @action(detail=True, methods=["post"], url_path="unpublish")
    def unpublish(self, request, pk=None):
        lesson = self.get_object(pk)
        if lesson.course.owner != request.user:
            return Response(status=403)
        if not lesson.is_published:
            return Response({"detail": "already unpublished"}, status=400)

        lesson.is_published = False
        lesson.save(update_fields=["is_published"])
        return Response(LessonSerializer(lesson).data)

