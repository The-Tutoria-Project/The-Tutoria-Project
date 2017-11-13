import json


from main.forms import UserForm, StudentInfoForm, BookingForm, TutorInfoForm, AddToWallet
from . import models
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response, redirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic import View, ListView, DetailView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from main.models import Availability, Sessions, Student, Tutor, Course, Wallet
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class IndexView(TemplateView):
    template_name = 'index.html'


def signup(request):
    return render(request, 'signup.html', {})


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'index.html', {})


# Authorisation view using the built in Django authorisation model.
def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        # Student_form=StudentInfoForm(data=request.POST)

        if user_form.is_valid():
            # and Student_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

            login(request, user)

            print(user.username)
            render(request, 'main/registration.html',
                   {'user': user, 'registered': registered})

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render(request, 'main/registration.html', {'user_form': user_form, 'registered': registered})


# Authorisation view using the built in Django authorisation model.
def studentRegistration(request):
    registered = False
    uid = request.GET['value1']
    print(request.user)

    if request.method == "POST":

        Student_form = StudentInfoForm(data=request.POST)

        if Student_form.is_valid():

            Student = Student_form.save(commit=False)
            print(Student)
            print("HEreeee")

            Student.user = request.user
            print(request.user)

            if 'profile_pic' in request.FILES:
                Student.profile_pic = request.FILES['profile_pic']

            Student.save()

            registered = True

        else:
            print(Student_form.errors)

    else:
        # user_form=UserForm()
        Student_form = StudentInfoForm()

    return render(request, 'main/studentreg.html', {'Student_form': Student_form, 'registered': registered, 'user': request.user})


# Authorisation view using the built in Django authorisation model.
def register2(request):
    registered = False
    uid = request.GET['value1']
    print(User.objects.get(username=uid))

    if request.method == "POST":

        Tutor_form = TutorInfoForm(data=request.POST)

        if Tutor_form.is_valid():

            tutorInst = Tutor_form.save(commit=False)
            tutorInst.user = request.user

            # if 'profile_pic' in request.FILES:
            #     Student.profile_pic=request.FILES['profile_pic']

            tutorInst.save()

            registered = True

        else:
            print(Tutor_form.errors)

    else:
        # user_form=UserForm()
        Tutor_form = TutorInfoForm()

    return render(request, 'main/tutorreg.html', {'Tutor_form': Tutor_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(str(user))
        if user:
            if user.is_active:
                login(request, user)
                return render(request, 'main/home.html', {})
                # return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT INACTIVE")
        else:
            print("Login failed")
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'main/login.html', {})


class TutorListView(ListView):

    context_object_name = 'tutors'
    model = models.Tutor


class TutorDetailView(DetailView):
    context_object_name = 'tutor_details'
    model = models.Tutor
    template_name = 'main/tutor_detail.html'


@login_required
def bookSession(request):

    current_user = request.user
    print(current_user.id)
    # basically if there is a post request take that student_id, tutor id and time slot and save it in session.
    form = request.POST
    tutorID = request.GET["value1"]

    sid = Student.objects.get(user=current_user)

    tutor = Tutor.objects.get(id=tutorID)  # get tutor object

    slot = Availability.objects.filter(tutor_id=tutorID, isAvailable=True)

    if not slot:
        return HttpResponse('<em> Oops! This Tutor has no available time slots </em>')

    else:
        if request.method == 'POST':
            selectedSlot = get_object_or_404(Availability, pk=request.POST.get(
                'slot_id'))  # get user's selected slot from the drop down

            try:
                Sessions_instance = Sessions.objects.create(
                    tutorID=tutor, studentID=sid, bookedTime=selectedSlot, sessionAmount=100)  # add the new session to the db table
                selectedSlot.isAvailable = False  # make the slot unavailable
                selectedSlot.save()  # save the slot
                balance = sid.wallet - tutor.hourly_rate
                sid.wallet = balance
                sid.save()
                print(balance)
                return render(request, 'main/home.html', {})
                # return HttpResponse("Your Session is Successfully Booked!")

            except ValidationError as e:
                return JsonResponse({'status': 'false', 'message': 'You have another session at the same time or already have a session with this tutor today!'}, status=500)
    # return render(request, self.template_name, {'slots': slot})
    return render(request, 'main/session.html', {'slots': slot, 'tutor': tutor, 'balance': sid})


@login_required
def mySessions(request):

    currentStudent = request.user
    print(currentStudent.id)
    student = Student.objects.get(user=currentStudent)
    bookedSlots = Sessions.objects.filter(studentID_id=student.id)

    if not bookedSlots:
        return HttpResponse('<em> Oops! You have no sessions booked currently</em>')

    if request.method == 'POST':
        print(request.POST.get('bookedSlots_id'))
        slotToCancel = get_object_or_404(
            Sessions, pk=request.POST.get('bookedSlots_id'))
        Availability.objects.filter(sessionKey__bookedTime=slotToCancel.bookedTime,
                                    tutor_id=slotToCancel.tutorID, isAvailable=False).update(isAvailable=True)

        slotToCancel.delete()
        return render(request, 'main/home.html', {})
    return render(request, 'main/mySessions.html', {'bookedSlots': bookedSlots})


def homePage(request):
    return render(request, 'main/home.html')


# def studentreg(request):
#     return render(request, 'main/studentreg.html')

@login_required
def search(request):

    if request.method == 'GET':
        userText = request.GET.get('search_box')
        print(userText)
        search = Tutor.objects.filter(
            Q(firstName=userText) | Q(lastName=userText))
        print(search)
        return render(request, 'main/search.html', {'tutors': search})

    return render(request, 'main/search.html')


def myWallet(request):

    currentUser = request.user
    wallet = Wallet.objects.get(user= currentUser)
    student = Student.objects.get(user= currentUser)

    if request.method == "POST":

        walletForm = AddToWallet(data=request.POST)

        if walletForm.is_valid():

            wallet.amount += walletForm.cleaned_data['amount']
            wallet.save()    

        else:
            print(walletForm.errors)

    else:
        walletForm = AddToWallet()

    tminus30days = datetime.today() - timedelta(days=30)
    transactionList = Sessions.objects.filter(studentID= student, bookedTime__date__gt=tminus30days)



    return render(request, 'main/wallet.html', {'wallet':wallet, 'user':currentUser, 'sessions':transactionList, 'walletForm': walletForm})

'''def cancelSession(request):




    def tutor_detail_view(request,pk):
        try:
            tutor_id=Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Book does not exist")

        #book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'main/tutor_detail.html',
            context={'tutor_details':tutor_id,}'''
