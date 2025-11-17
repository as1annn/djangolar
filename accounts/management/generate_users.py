import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from faker import Faker

class Command(BaseCommand):
    help = "Generate random users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=10,
            help="Number of users to create",
        )

    def handle(self, *args, **options):
        number_of_users = options["number"]
        User = get_user_model()
        fake = Faker()

        roles = ["admin", "manager", "employee"]
        departments = ["IT", "HR", "Sales", "Finance"]

        for _ in range(number_of_users):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            username = fake.user_name()
            phone = fake.phone_number()
            city = fake.city()
            country = fake.country()
            department = random.choice(departments)
            role = random.choice(roles)
            birth_date = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=65)
            salary = random.randint(30000, 150000)
            password = make_password("defaultpassword")

            user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                city=city,
                country=country,
                department=department,
                role=role,
                birth_date=birth_date,
                salary=salary,
                password=password,
                is_active=True,
            )
            user.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully created {number_of_users} users"))
