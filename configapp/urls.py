from rest_framework.routers import DefaultRouter
from configapp.veiws import *
from django.urls import path,include
router = DefaultRouter()
router.register(r'teachers',TeacherCreateApi)
router.register(r'department',DepartmentAPI)
router.register(r'course',CourseAPI)
router.register(r'student',StudentDetailApi)
router.register(r'group',AddGroupAPI)
router.register(r'table',AddTableAPI)
router.register(r'room',RoomsAPI)
router.register(r'tabletype',TableTypeAPI)

urlpatterns = [
    path('',include(router.urls)),
    path('send_sms/',SendEmailAPI.as_view()),
    path("change-password/", StudentChangePassword.as_view(), name="change-password"),
    path('login_user_token/',LoginUser.as_view()),
    # path('register/',RegisterApi.as_view()),
]