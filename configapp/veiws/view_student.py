from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework.views import APIView
from configapp.make_token import get_tokens_for_user
from drf_yasg.utils import swagger_auto_schema
from configapp.Permission import IsEmailVerified, IsAdmin
from configapp.models import *
from configapp.serializers import StudentSerializer, UserSerializer, StudentAndUserSerializer, ChangePasswordSerializer, LoginSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
class StudentDetailApi(ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [IsEmailVerified, IsAdmin]
    def get_permissions(self):
        if self.action in ["list", "retrieve", "update", "destroy"]:
            return [IsAdmin()]
        return [IsAdmin()]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "update", "destroy"]:
            return StudentSerializer
        return StudentAndUserSerializer

    def create(self,request,*args,**kwargs):
        user_data = request.data.get('user',None)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save(is_student=True, is_active=False)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        student = request.data.get('student',None)
        student_serializer = StudentSerializer(data=student)
        if student_serializer.is_valid(raise_exception=True):
            student_serializer.save(user = user)
        else:
            user.delete()
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "user": user_serializer.data,
            "student": student_serializer.data
        }, status=status.HTTP_201_CREATED)

class StudentChangePassword(APIView):
    permission_classes = [IsAdmin]
    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        otp = serializer.validated_data.get("otp")
        new_password = serializer.validated_data.get("new_password")
        cached_otp = cache.get(f"{email}_otp")
        if not cached_otp or cached_otp != otp:
            return Response(
                {"message": "OTP noto'g'ri yoki muddati tugagan"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "Foydalanuvchi topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )
        user.set_password(new_password)
        user.is_active = True
        user.save()
        cache.delete(f"{email}_otp")
        return Response(
            {"message": "Parol muvaffaqiyatli o'zgartirildi"},
            status=status.HTTP_200_OK
        )


class LoginUser(APIView):
    @swagger_auto_schema(request_body=LoginSerializers)
    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "Email yoki parol noto'g'ri"}, status=400)
        if not user.is_active:
            return Response({"error": "User active emas"}, status=403)
        token = get_tokens_for_user(user)
        return Response(token, status=200)


