from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from test_django.forms import SubjectForm, SchoolForm, StudentForm
from test_django.models import Student, Subject, Teacher, School


def show_info(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="Teachers").exists():
            teacher = Teacher.objects.get(id_user_id=user.id)
            subjects = Subject.objects.filter(teacher=teacher.id)
            subjects = list(subjects)
            return render(request, 'teacherInfo.html',
                          {"teacher": teacher, "subjects": subjects})
        student = Student.objects.get(id_user_id=user.id)
        subjects = Subject.objects.filter(student=student.id)
        subjects = list(subjects)
        return render(request, 'studentInfo.html',
                      {"student": student, "subjects": subjects})
    else:
        return render(request, 'noAccess.html')


def show_sign(request):
    current_user = request.user
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect('info/')
        return render(request, 'sign.html', {})
    else:
        if request.POST.get("email") != None:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_tmp = User.objects.get(email=email)
            if not user_tmp.check_password(password):
                return redirect('/')
            if Student.objects.filter(id_user_id=user_tmp.id).exists() \
                    or Teacher.objects.filter(id_user_id=user_tmp.id).exists():
                user = authenticate(username=user_tmp.username, password=password)
                login(request, user_tmp)
            else:
                user = authenticate(username=user_tmp.username, password=password)
                obj = Student.objects.create(
                    first_name=user_tmp.username,
                    id_user_id=user.id
                )
                obj.save()
                login(request, user)
            return redirect("/info")
        else:
            email = request.POST.get('email_reg')
            password = request.POST.get('password_reg')
            name = request.POST.get('username_reg')
            obj = User.objects.create_user(email=email,
                                            username=name,
                                            password=password)
            return redirect("/")


def show_base(request):
    return render(request, 'base.html', {})


def edit_profile(request, id_user):
    print(id_user)
    if request.method == "GET":
        student_form = StudentForm()
        student = Student.objects.get(id=id_user)
        return render(request, 'formTemplate.html', {'form': student_form, 'student': student})
    else:
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student = Student.objects.get(id=id_user)
            student.first_name = student_form.cleaned_data['first_name']
            student.surname = student_form.cleaned_data['surname']
            student.phone_number = student_form.cleaned_data['phone_number']
            student.save()
            subjects = Subject.objects.filter(student=student.id)
            subjects = list(subjects)
            return render(request, 'studentInfo.html',
                          {"student": student, "subjects": subjects})
        else:
            redirect('info/')

def schools_info(request, teacher_id):
    user = request.user
    if user.groups.filter(name="Teachers").exists():
        teacher = Teacher.objects.get(id=teacher_id)
        schools = teacher.school.all()
        return render(request, 'schoolsInfo.html',
                      {"teacher": teacher, "schools": schools})
    else:
        return render(request, 'noAccess.html')


def create_school(request, teacher_id):
    if request.method == "GET":
        school_form = SchoolForm()
        return render(request, 'createSchool.html', {'form': school_form})
    else:
        school_form = SchoolForm(request.POST)
        if school_form.is_valid():
            obj = School.objects.create(
                type=school_form.cleaned_data['type'],
                address=school_form.cleaned_data['address'],
                rating=school_form.cleaned_data['rating'],
            )
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.school.add(obj)
            return redirect(f"/info/{teacher_id}/schools")
        else:
            return render(request, 'noAccess.html')


def show_student(request, id_user):
    user = request.user
    if user.is_authenticated:
        student = Student.objects.get(id_user_id=id_user)
        subjects = Subject.objects.filter(student=student.id)
        subjects = list(subjects)
        return render(request, 'studentInfo.html',
                      {"student": student, "subjects": subjects})
    else:
        return render(request, 'noAccess.html')


def delete_subject(request, subject_id):
    user = request.user
    if user.groups.filter(name="Teachers").exists():
        subject = Subject.objects.get(id=subject_id)
        subject.delete()
        teacher = Teacher.objects.get(id_user_id=user.id)
        subjects = Subject.objects.filter(teacher=teacher.id)
        subjects = list(subjects)
        return redirect(f"/info/")
    else:
        return render(request, 'noAccess.html')


def create_subject(request, teacher_id):
    current_user = request.user
    if request.method == "GET":
        subject_form = SubjectForm()
        return render(request, 'formTemplate.html', {'form': subject_form})
    else:
        subject_form = SubjectForm(request.POST)
        if subject_form.is_valid():
            obj = Subject.objects.create(
                name=subject_form.cleaned_data['name'],
                mark=subject_form.cleaned_data['mark'],
                student=subject_form.cleaned_data['student'],
                teacher_id=Teacher.objects.get(id_user=current_user.id).id
            )
            return redirect(f"/info/")
        else:
            return render(request, 'noAccess.html')


def validate_mark(request):
    mark = int(request.GET.get('mark', None))
    response = {
        'mark_neg': mark < 1,
        'mark_high': mark > 5
    }
    return JsonResponse(response)


def validate_name_mail(request):
    name = request.GET.get('username_reg', None)
    mail = request.GET.get('email_reg', None)
    response = {
        'taken_name': User.objects.filter(username__exact=name).exists(),
        'taken_mail': User.objects.filter(email__exact=mail).exists(),
    }
    return JsonResponse(response)