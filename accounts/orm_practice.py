from datetime import date, timedelta

from django.db import models
from django.db.models import (
    Q,
    Count,
    Avg,
    Max,
    Min,
    Case,
    When,
    Value,
    CharField,
    F,
    Sum,
    ExpressionWrapper,
    DurationField,
)
from django.db.models.functions import ExtractYear
from django.utils import timezone

from .models import CustomUser


q_2_1 = CustomUser.objects.filter(is_active=True)

q_2_2 = CustomUser.objects.filter(email__iendswith="@gmail.com")

q_2_3 = CustomUser.objects.filter(city="Almaty")

q_2_4 = CustomUser.objects.exclude(city="Almaty")

q_2_5 = CustomUser.objects.filter(salary__gt=500000)

q_2_6 = CustomUser.objects.filter(department="IT", country="Kazakhstan")

q_2_7 = CustomUser.objects.filter(birth_date__isnull=True)

q_2_8 = CustomUser.objects.filter(first_name__istartswith="A")

q_2_9 = CustomUser.objects.count()

q_2_10 = CustomUser.objects.order_by("-date_joined")[:20]

q_2_11 = CustomUser.objects.values_list("city", flat=True).distinct()

q_2_12 = CustomUser.objects.filter(department="Sales").count()

seven_days_ago = timezone.now() - timedelta(days=7)
q_2_13 = CustomUser.objects.filter(last_login__gte=seven_days_ago)

q_2_14 = CustomUser.objects.filter(
    Q(first_name__icontains="bek") | Q(last_name__icontains="bek")
)

q_2_15 = CustomUser.objects.filter(salary__gte=300000, salary__lte=700000)

q_2_16 = CustomUser.objects.filter(department__in=["IT", "HR", "Finance"])

q_2_17 = CustomUser.objects.values("department").annotate(
    user_count=Count("id")
)

q_2_18 = CustomUser.objects.values("department").annotate(
    user_count=Count("id")
).order_by("-user_count")

q_2_19 = (
    CustomUser.objects.values("city")
    .annotate(user_count=Count("id"))
    .order_by("-user_count")[:5]
)

q_2_20 = CustomUser.objects.filter(last_login__isnull=True)

q_2_21 = CustomUser.objects.aggregate(avg_salary=Avg("salary"))

q_2_22 = CustomUser.objects.aggregate(
    max_salary=Max("salary"),
    min_salary=Min("salary"),
)

q_2_23 = CustomUser.objects.filter(phone__contains="+7")

q_2_24 = CustomUser.objects.annotate(
    full_name=F("first_name") + Value(" ") + F("last_name")
)

q_2_25 = CustomUser.objects.annotate(
    birth_year=ExtractYear("birth_date")
).order_by("birth_year")

q_2_26 = CustomUser.objects.filter(birth_date__month=5)

q_2_27 = CustomUser.objects.filter(role="manager", salary__gt=400000)

q_2_28 = CustomUser.objects.filter(Q(role="employee") | Q(department="HR"))

q_2_29 = (
    CustomUser.objects.filter(is_active=True)
    .values("city")
    .annotate(active_count=Count("id"))
)

q_2_30 = CustomUser.objects.order_by("date_joined")[:10]

q_2_31 = CustomUser.objects.filter(city__istartswith="A", salary__gt=300000)

q_2_32 = CustomUser.objects.filter(Q(department__isnull=True) | Q(department=""))

q_2_33 = (
    CustomUser.objects.values("country")
    .annotate(
        user_count=Count("id"),
        avg_salary=Avg("salary"),
    )
)

q_2_34 = CustomUser.objects.filter(is_staff=True).order_by("-last_login")

q_2_35 = CustomUser.objects.exclude(email__icontains="example.com")

avg_salary_value = CustomUser.objects.aggregate(avg_salary=Avg("salary"))["avg_salary"]
q_2_36 = CustomUser.objects.filter(salary__gt=avg_salary_value)

q_2_37 = (
    CustomUser.objects.values("email")
    .annotate(email_count=Count("id"))
    .filter(email_count__gt=1)
)

q_2_38 = CustomUser.objects.annotate(
    salary_level=Case(
        When(salary__lt=300000, then=Value("low")),
        When(salary__gte=300000, salary__lte=700000, then=Value("medium")),
        When(salary__gt=700000, then=Value("high")),
        default=Value("unknown"),
        output_field=CharField(),
    )
).order_by("salary_level")

current_year = timezone.now().year
q_2_39 = CustomUser.objects.filter(date_joined__year=current_year)

q_2_40 = (
    CustomUser.objects.values("department")
    .annotate(total_salary=Sum("salary"))
)

q_2_41 = CustomUser.objects.filter(department="IT", last_login__isnull=True)

q_2_42 = CustomUser.objects.filter(
    country="Kazakhstan"
).filter(Q(city__isnull=True) | Q(city=""))

q_2_43 = CustomUser.objects.filter(
    birth_date__lt=date(1990, 1, 1),
    salary__isnull=False,
)

q_2_44 = CustomUser.objects.annotate(
    time_since_joined=ExpressionWrapper(
        timezone.now() - F("date_joined"),
        output_field=DurationField(),
    )
)

q_2_45 = CustomUser.objects.filter(
    department="Sales",
    email__iendswith="@gmail.com",
    salary__gt=350000,
)

q_2_46 = CustomUser.objects.order_by("country", "-salary")

q_2_47 = (
    CustomUser.objects.values("role")
    .annotate(user_count=Count("id"))
    .filter(user_count__gt=100)
)

q_2_48 = CustomUser.objects.filter(
    last_login__lt=F("date_joined"),
    last_login__isnull=False,
)

q_2_49 = CustomUser.objects.annotate(
    is_senior=Case(
        When(birth_date__lt=date(1985, 1, 1), then=Value(True)),
        default=Value(False),
        output_field=models.BooleanField(),
    )
)

q_2_50 = (
    CustomUser.objects.values("department")
    .annotate(
        user_count=Count("id"),
        avg_salary=Avg("salary"),
    )
    .filter(user_count__gte=20)
    .order_by("-avg_salary")
)
