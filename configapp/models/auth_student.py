from .auth_user import *
from .model_group import *

class Student(BaseModel):
    full_name = models.CharField()
    user=models.OneToOneField(User ,on_delete=models.CASCADE)
    group = models.ManyToManyField(GroupStudent,related_name='get_group')
    is_line =models.BooleanField(default=False)
    descriptions = models.TextField(blank=True,null=True)


    def __str__(self):
        return self.full_name

class Parents(BaseModel):
    student = models.OneToOneField(Student,on_delete=models.CASCADE,related_name='student')
    full_name = models.CharField(max_length=50,null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    descriptions = models.CharField(max_length=500,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.full_name
