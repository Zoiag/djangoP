from django.db import models
from django.contrib.auth.models import User


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(**kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
''''''

class School(models.Model):
    type = models.TextField(verbose_name="Type of school", help_text="Enter a type", null=False, blank=False)

    address = models.TextField(verbose_name="Address", help_text="Enter an address",
                               null=False, blank=False)
    rating = IntegerRangeField(max_value=10, min_value=0, verbose_name="0 to 10",
                               help_text="Choose a rating", null=False, blank=False)

    def __str__(self):
        return "School address: " + self.address

    class Meta:
        db_table = "School"


class Teacher(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="First Name", help_text="Enter a first name",
                                  null=False, blank=False)
    surname = models.CharField(max_length=50, verbose_name="Surname", help_text="Enter a surname",
                               null=False, blank=False)
    experience = IntegerRangeField(max_value=100, min_value=0, verbose_name="Experience",
                                   help_text="Choose an experience", null=False, blank=False)
    school = models.ManyToManyField(School, verbose_name="School",
                               help_text="Choose a school", null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Id User", help_text="Choose an id user",
                                null=True, blank=True)

    def __str__(self):
        return "Teacher: " + self.surname + " " + self.first_name + ". Experience: " + str(self.experience) + ". " \
               + self.school.__str__()

    class Meta:
        db_table = "Teacher"


class Student(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="First Name", help_text="Enter a first name",
                                  null=False, blank=False)
    surname = models.CharField(max_length=50, verbose_name="Surname", help_text="Enter a surname",
                               null=False, blank=False)
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number", help_text="Enter a phone number",
                                    null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Id User", help_text="Choose an id user",
                                null=True, blank=True)

    def __str__(self):
        return "Student: " + self.surname + " " + self.first_name

    class Meta:
        db_table = "Student"


class Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name", help_text="Enter a name",
                            null=False, blank=False)
    mark = IntegerRangeField(max_value=5, min_value=1, verbose_name="Mark", help_text="Enter a mark",
                             null=False, blank=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Teacher",
                                help_text="Choose a teacher", null=True, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Student",
                                help_text="Choose a student", null=False, blank=False)

    def __str__(self):
        return "Subject: " + self.name

    class Meta:
        db_table = "Subject"


# Create your models here.

