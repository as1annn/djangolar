from django.db import models
from decimal import Decimal
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class SoftDeleteModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()              
    all_objects = SoftDeleteQuerySet.as_manager()  

    class Meta:
        abstract = True   

    def delete(self, using=None, keep_parents=False):
        
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])


class Course(SoftDeleteModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)  
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_courses',
    )

    def __str__(self):
        return self.title


class Lesson(SoftDeleteModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    title = models.CharField(max_length=255)
    content = models.TextField()


    order = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))


    indentation = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(5)],
    )

    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.course.title}"
