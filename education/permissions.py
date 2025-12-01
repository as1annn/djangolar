from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Course, Lesson

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        from .models import Course
        if isinstance(obj, Course):
            return obj.owner.id == user.id
        if isinstance(obj, Lesson):
            return obj.course.owner.id == user.id
        return False
    