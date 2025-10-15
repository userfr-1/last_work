from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/group/<int:pk>/', views.teacher_group_detail, name='teacher_group_detail'),
    path('teacher/lesson/add/', views.add_lesson, name='lesson_add'),
    path('teacher/lesson/<int:pk>/edit/', views.edit_lesson, name='lesson_edit'),
    path('teacher/lesson/<int:pk>/delete/', views.delete_lesson, name='lesson_delete'),
    path('teacher/homework/<int:lesson_id>/add/', views.add_homework, name='homework_add'),
    path('teacher/homework_uploads/', views.homework_list, name='homework_list'),
    path('teacher/homework_upload/<int:pk>/check/', views.check_homework, name='check_homework'),
    path('teacher/attendance/', views.attendance_manage, name='attendance_manage'),
    path('teacher/resource/add/', views.resource_add, name='resource_add'),
    path('teacher/report/', views.teacher_report, name='teacher_report'),


    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/group/<int:pk>/', views.student_group_detail, name='student_group_detail'),
    path('student/lessons/', views.student_lessons, name='student_lessons'),
    path('student/lesson/<int:pk>/', views.student_lesson_detail, name='lesson_detail'),
    path('student/homework/<int:homework_id>/upload/', views.homework_upload, name='homework_upload'),
    path('student/payments/', views.student_invoice, name='student_invoice'),
    path('student/attendance/', views.student_attendance, name='student_attendance'),
    path('student/resources/', views.student_resources, name='student_resources'),
]
