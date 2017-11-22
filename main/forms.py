from django import forms
from django.contrib.auth.models import User
from main.models import Student, Sessions, Tutor


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password')
        # remove email


class StudentInfoForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ('firstName', 'lastName', 'email')


class TutorInfoForm(forms.ModelForm):
    class Meta():
        model = Tutor
        fields = ('firstName', 'lastName', 'tutor_email', 'courses',
                  'university_name', 'hourly_rate', 'tutor_intro', 'isStudent','phoneNo', 'searchTags', 'avatar', 'tutorType')


class BookingForm(forms.ModelForm):
    class Meta():
        model = Sessions
        fields = ('tutorID', 'studentID', 'bookedDate', 'bookedStartTime', 'bookedEndTime')
