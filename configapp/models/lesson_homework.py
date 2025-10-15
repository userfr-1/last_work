from django.db import models
from .auth_user import BaseModel
from .auth_teacher import Teacher
from .auth_student import Student
from .model_group import GroupStudent

class Homework(BaseModel):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.title or f"Homework #{self.id}"

class Lesson(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons')
    homework = models.OneToOneField(Homework, on_delete=models.SET_NULL, blank=True, null=True, related_name='lesson')
    video_url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='lessons/files/', blank=True, null=True)
    image = models.ImageField(upload_to='lessons/images/', blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.group.title})"

class HomeworkUpload(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='homework_uploads')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='uploads')
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='student_homework/files/', blank=True, null=True)
    photo = models.FileField(upload_to='student_homework/photos/', blank=True, null=True)
    mark = models.SmallIntegerField(blank=True, null=True)
    is_checked = models.BooleanField(default=False)

    STATUS_CHOICES = (
        ('not_submitted', 'Berilmagan'),
        ('pending', 'Kutayotgan'),
        ('accepted', 'Qabul qilingan'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_submitted')

    def __str__(self):
        return f"{self.student.full_name} → {self.homework.title or 'Homework'}"
