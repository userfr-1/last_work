from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserRegisterForm, UserLoginForm
from .models import *

def register_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ro‘yxatdan o‘tish muvaffaqiyatli! Endi tizimga kiring.")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "auth/register.html", {"form": form})

#
# def login_view(request):
#
#     if request.method == "POST":
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(email=email, password=password)
#
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f"Xush kelibsiz, {user.email}!")
#
#
#                 if user.is_teacher:
#                     return redirect("teacher_dashboard")
#                 elif user.is_student:
#                     return redirect("student_dashboard")
#                 elif user.is_admin:
#                     return redirect("/admin/")
#             else:
#                 messages.error(request, "Email yoki parol noto‘g‘ri!")
#     else:
#         form = UserLoginForm()
#
#     return render(request, "auth/login.html", {"form": form})
#
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserLoginForm

def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.email}!")

                if getattr(user, "is_teacher", False):
                    return redirect("teacher_dashboard")
                elif getattr(user, "is_student", False):
                    return redirect("student_dashboard")
                elif getattr(user, "is_admin", False) or user.is_superuser:
                    return redirect("/admin/")
                else:
                    return redirect("/")  # fallback
            else:
                messages.error(request, "Email yoki parol noto‘g‘ri!")
    else:
        form = UserLoginForm()

    return render(request, "auth/login.html", {"form": form})



@login_required
def logout_view(request):
    """Tizimdan chiqish"""
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect("login")


from django.shortcuts import render
from .models import GroupStudent, Lesson, Resource, HomeworkUpload


def teacher_dashboard(request):
    teacher = request.user.teacher

    groups = GroupStudent.objects.filter(teacher=teacher)
    lessons = Lesson.objects.filter(teacher=teacher)
    resources = Resource.objects.filter(uploaded_by=teacher.user)
    homework_uploads = HomeworkUpload.objects.filter(homework__lesson__teacher=teacher)

    context = {
        'teacher': teacher,
        'groups': groups,
        'lessons': lessons,
        'resources': resources,
        'homework_uploads': homework_uploads,
    }
    return render(request, 'teacher/dashboard.html', context)

def teacher_group_detail(request, pk):
    group = get_object_or_404(GroupStudent, pk=pk)

    students = Student.objects.filter(group=group)

    lessons = Lesson.objects.filter(group=group)

    context = {
        'group': group,
        'students': students,
        'lessons': lessons
    }
    return render(request, 'teacher/group_detail.html', context)


@login_required
def add_lesson(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description')
        group_id = request.POST['group']
        group = GroupStudent.objects.get(id=group_id)
        Lesson.objects.create(title=title, description=description, group=group, teacher=teacher)
        return redirect('teacher_dashboard')
    groups = GroupStudent.objects.all()
    return render(request, 'teacher/add_lesson.html', {'groups': groups})


@login_required
def edit_lesson(request, pk):
    lesson = get_object_or_404(Lesson, id=pk)
    if request.method == 'POST':
        lesson.title = request.POST['title']
        lesson.description = request.POST['description']
        lesson.save()
        return redirect('teacher_dashboard')
    return render(request, 'teacher/edit_lesson.html', {'lesson': lesson})


@login_required
def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, id=pk)
    lesson.delete()
    return redirect('teacher_dashboard')


@login_required
def add_homework(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Homework.objects.create(title=title, description=description, lesson=lesson)
        return redirect('teacher_dashboard')
    return render(request, 'teacher/add_homework.html', {'lesson': lesson})


@login_required
def homework_list(request):
    uploads = HomeworkUpload.objects.filter(homework__lesson__teacher__user=request.user)
    return render(request, 'teacher/homework_list.html', {'uploads': uploads})

@login_required
def check_homework(request, pk):

    upload = get_object_or_404(HomeworkUpload, id=pk)

    if upload.homework.lesson.teacher != request.user.teacher:
        messages.error(request, "Siz bu topshiriqni baholay olmaysiz!")
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        upload.status = request.POST.get('status')
        upload.mark = request.POST.get('mark')
        upload.is_checked = True
        upload.save()

        messages.success(request, "Topshiriq baholandi va saqlandi!")
        return redirect('teacher_dashboard')


    return render(request, 'teacher/check_homework.html', {'upload': upload})



@login_required
def attendance_manage(request):
    groups = GroupStudent.objects.all()
    return render(request, 'teacher/attendance_manage.html', {'groups': groups})


@login_required
def teacher_report(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    lessons = Lesson.objects.filter(teacher=teacher)
    uploads = HomeworkUpload.objects.filter(homework__lesson__teacher=teacher)
    return render(request, 'teacher/report.html', {'teacher': teacher, 'lessons': lessons, 'uploads': uploads})

@login_required
def resource_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        course_id = request.POST.get('course')
        file = request.FILES.get('file')
        teacher = get_object_or_404(Teacher, user=request.user)

        if title and course_id and file:

            from .models import Resource, Course
            course = get_object_or_404(Course, id=course_id)
            Resource.objects.create(title=title, course=course, file=file, teacher=teacher)
            return redirect('teacher_dashboard')


    from .models import Course
    courses = Course.objects.all()
    return render(request, 'teacher/resource_add.html', {'courses': courses})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, GroupStudent, Lesson, Homework, HomeworkUpload

@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    groups = student.group.all()

    # Agar student hech bir guruhga biriktirilmagan bo‘lsa:
    if not groups.exists():
        messages.warning(request, "Siz hali birorta guruhga biriktirilmagansiz.")
        lessons = []
    else:
        lessons = Lesson.objects.filter(group__in=groups)

    uploads = HomeworkUpload.objects.filter(student=student)

    return render(request, 'student/dashboard.html', {
        'student': student,
        'groups': groups,
        'lessons': lessons,
        'homework_uploads': uploads,
    })


@login_required
def student_group_detail(request, pk):
    group = get_object_or_404(GroupStudent, id=pk)
    lessons = group.lessons.all() if hasattr(group, 'lessons') else []
    return render(request, 'student/group_detail.html', {
        'group': group,
        'lessons': lessons,
    })


@login_required
def student_lessons(request):
    student = get_object_or_404(Student, user=request.user)
    groups = student.group.all()
    lessons = Lesson.objects.filter(group__in=groups)
    return render(request, 'student/lessons.html', {'lessons': lessons})


@login_required
def student_lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, id=pk)
    return render(request, 'student/lesson_detail.html', {'lesson': lesson})


@login_required
def homework_upload(request, homework_id):
    student = get_object_or_404(Student, user=request.user)
    homework = get_object_or_404(Homework, id=homework_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        file = request.FILES.get('file')
        HomeworkUpload.objects.create(
            student=student,
            homework=homework,
            text=text,
            file=file,
            status='pending'
        )
        return redirect('student_dashboard')
    return render(request, 'student/homework_upload.html', {'homework': homework})


@login_required
def student_invoice(request):
    student = get_object_or_404(Student, user=request.user)
    payments = getattr(student, 'payments', []).all() if hasattr(student, 'payments') else []
    return render(request, 'student/payments.html', {'payments': payments})


@login_required
def student_attendance(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'student/attendance.html', {'student': student})


@login_required
def student_resources(request):
    student = get_object_or_404(Student, user=request.user)
    groups = student.group.all()
    lessons = Lesson.objects.filter(group__in=groups)
    return render(request, 'student/resources.html', {'lessons': lessons})
