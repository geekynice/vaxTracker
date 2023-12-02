from django.db import models
import uuid
from datetime import datetime
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from django.contrib.auth.models import AbstractUser
# Create your models here.


class FamilyModel(DjangoCassandraModel):
    house_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    address = columns.Text()
    family_member_ids = columns.List(columns.UUID())  # List of member IDs
    total_people = columns.Integer()
    total_vaccinated = columns.Integer()
    total_adults = columns.Integer()
    total_infants = columns.Integer()
    doctor_assigned = columns.Text()

    def __str__(self):
        return f"Family {self.house_id}"

class FamilyMemberModel(DjangoCassandraModel):
    member_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(required=True)
    age = columns.Integer(required=True)
    gender = columns.Text(required=True)
    vaccination_status = columns.Boolean(default=False)
    vaccine_received = columns.Text()
    house_id = columns.UUID()

    @classmethod
    def get_members_by_house(cls, house_id):
        return cls.objects.filter(house_id=house_id)


    def __str__(self):
        return f"{self.name} (ID: {self.member_id})"


class UserModel(DjangoCassandraModel):
    user_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    username = columns.Text(required=True)
    password = columns.Text(required=True)
    email = columns.Text(required=True)
    created_at = columns.DateTime(default=datetime.now)
    role = columns.Text(required=True)

    def __str__(self):
        return f"{self.role} - {self.username} (ID: {self.user_id})"

class DoctorModel(UserModel):
    doctor_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(required=True)
    phone_number = columns.Text()
    address = columns.Text()
    post = columns.Text()
    specialization = columns.Text()


    class Meta:
        get_pk_field = 'doctor_id'


    def __str__(self):
        return f"Dr. {self.name} (ID: {self.doctor_id})"

class AdminModel(UserModel):

    def __str__(self):
        return f"Admin - {self.username} (ID: {self.user_id})"