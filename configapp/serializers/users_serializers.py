from rest_framework import serializers
from configapp.models import *

class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_teacher = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_student = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'is_active', 'password', 'is_student', 'is_teacher', 'is_admin']
        read_only_fields = ['password']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        read_only_fields = ['user']
class ChangePasswordSerializer(serializers.Serializer):
    email  = serializers.EmailField()
    old_password=serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    otp = serializers.CharField()

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("Parollar bir xil emas")
        return attrs
class TeacherAndUserSerializer(serializers.Serializer):
    user = UserSerializer()
    teacher = TeacherSerializer()

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ['user']

class StudentAndUserSerializer(serializers.Serializer):
    user = UserSerializer()
    student = StudentSerializer()

class SendEmail(serializers.Serializer):
    email = serializers.EmailField()

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    verify_kod =serializers.CharField()

class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    verify_kod = serializers.CharField()

    def validate(self, data):
        user_id = data.get("id")
        password = data.get("password")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Bunday foydalanuvchi mavjud emas.")

        if not user.check_password(password):
            raise serializers.ValidationError("Parol noto‘g‘ri.")

        if not user.is_active:
            raise serializers.ValidationError("Foydalanuvchi faol emas.")

        data["user"] = user
        return data

class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()