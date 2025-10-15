from django.db import models
from .auth_user import BaseModel, User
from .model_group import GroupStudent

class Student(BaseModel):
    full_name = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ManyToManyField(GroupStudent, related_name='get_group', blank=True)
    is_line = models.BooleanField(default=False)
    descriptions = models.TextField(blank=True, null=True)

    def __str__(self): return self.full_name

class Parents(BaseModel):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='parent')
    full_name = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self): return self.full_name or f"Parent of {self.student.full_name}"
