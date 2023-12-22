from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms

from test_django.models import Subject, School, Student


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'mark', 'student')


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ('type', 'address', 'rating')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'surname', 'phone_number')


