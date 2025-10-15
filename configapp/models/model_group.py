from django.db import models
from .auth_user import BaseModel
from .auth_teacher import Course, Teacher

class Day(BaseModel):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self): return self.title

class Rooms(BaseModel):
    title = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self): return self.title

class TableType(BaseModel):
    title = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self): return self.title

class Table(BaseModel):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.ForeignKey(Rooms, on_delete=models.RESTRICT)
    type = models.ForeignKey(TableType, on_delete=models.RESTRICT)
    descriptions = models.TextField(blank=True, null=True)

    def __str__(self): return f"{self.start_time} - {self.end_time}"

class GroupStudent(BaseModel):
    title = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT, related_name='course_groups')
    teacher = models.ManyToManyField(Teacher, related_name='get_teacher', blank=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_time = models.DateField()
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self): return self.title
