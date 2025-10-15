from django.db import models
from .auth_user import BaseModel
from .auth_student import Student
from .model_group import GroupStudent

class Schedule(BaseModel):
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.group.title} - {self.day} {self.start_time}-{self.end_time}"

class Attendance(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    present = models.BooleanField(default=False)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'schedule', 'date')

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {'P' if self.present else 'A'}"
#pbkdf2_sha256$iteration$salts$hash
