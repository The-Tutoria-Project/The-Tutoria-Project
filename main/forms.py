from django import forms
from django.contrib.auth.models import User
from main.models import Student, Sessions, Tutor, Wallet


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password')
        # remove email


class StudentInfoForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ('firstName', 'lastName', 'wallet', 'email')


class TutorInfoForm(forms.ModelForm):
    class Meta():
        model = Tutor
        fields = ('firstName', 'lastName', 'tutor_email', 'courses', 'tutor_booking_status',
                  'university_name', 'hourly_rate', 'tutor_intro', 'isStudent','avatar', 'wallet')


class BookingForm(forms.ModelForm):
    class Meta():
        model = Sessions
        fields = ('tutorID', 'studentID', 'bookedTime', )

class AddToWallet(forms.ModelForm):
    class Meta():
        model = Wallet
        fields = ('amount',)
