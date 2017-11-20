import json


from main.forms import UserForm, StudentInfoForm, BookingForm, TutorInfoForm, AddToWallet
from . import models
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response, redirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic import View, ListView, DetailView, TemplateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from main.models import Availability, Sessions, Student, Tutor, Course, Wallet, SystemWallet
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from django.http import JsonResponse, Http404
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

            if 'avatar' in request.FILES:
                Student.avatar = request.FILES['profile_pic']

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

            if 'ava†ar' in request.FILES:
                Tutor.avatar = request.FILES['profile_pic']
            if (tutorInst.isStudent == True):
                Student_instance = Student.objects.create(
                    user=request.user, firstName=tutorInst.firstName, lastName=tutorInst.lastName, email=tutorInst.tutor_email, wallet=tutorInst.wallet)
                Student_instance.save()
            tutorInst.save()

            registered = True

        else:
            print(Tutor_form.errors)

    else:
        # user_form=UserForm()
        Tutor_form = TutorInfoForm()

    return render(request, 'main/tutorreg.html', {'Tutor_form': Tutor_form, 'registered': registered})


def choose_login(request):
    return render(request, 'Chooselogin.html', {})


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


def user_login1(request):  # For Tutor
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(str(user))
        if user:
            if user.is_active:

                try:
                    Tutor.objects.get(user=user)
                    login(request, user)
                    return render(request, 'main/WelcomeTutor.html', {})
                    # return HttpResponseRedirect(reverse('index'))

                except:
                    print("imposter")
                    return HttpResponse("Invalid login details")

            else:
                return HttpResponse("ACCOUNT INACTIVE")
        else:
            print("Login failed")
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'main/login1.html', {})


class TutorListView(ListView):

    context_object_name = 'tutors'
    model = models.Tutor


class TutorDetailView(DetailView):
    context_object_name = 'tutor_details'
    model = models.Tutor
    template_name = 'main/tutor_detail.html'


class TutorUpdateView(UpdateView):
    fields = ('tutor_email',)
    model = models.Tutor


@login_required
def bookSession(request):

    current_user = request.user
    tutorID = request.GET["value1"]
    sid = Student.objects.get(user=current_user)
    tutor = Tutor.objects.get(id=tutorID)  # get tutor object
    slot = Availability.objects.filter(tutor_id=tutorID)
    wallet = Wallet.objects.get(user=sid.user)
    currentDate = str(datetime.today().date())
    currentTime = str(datetime.now().hour) + ":" + str(datetime.now().minute)
    syswallet = SystemWallet.objects.get()
    sessions = Sessions.objects.filter(tutorID=tutorID)

    return render(request, 'main/session.html', {'slots': slot, 'tutor': tutor, 'balance': sid, 'currentDate': currentDate, 'currentTime': currentTime, 'sessions': sessions})


@login_required
def confirmedBooking(request):

    if request.method == 'POST':
        current_user = request.user
        tutorID = request.POST['tutID']
        tutor = Tutor.objects.get(id=tutorID)
        sid = Student.objects.get(user=current_user)

        slot = Availability.objects.filter(tutor_id=tutorID)
        wallet = Wallet.objects.get(user=sid.user)
        currentDate = str(datetime.today().date())
        currentTime = str(datetime.now().hour) + ":" + \
            str(datetime.now().minute)
        syswallet = SystemWallet.objects.get()
        sessions = Sessions.objects.filter(tutorID=tutorID)

        bookeddate_str = request.POST['bookeddate']
        startTime_str = request.POST['startTime']
        endTime_str = request.POST['endTime']

        bookedDate = datetime.strptime(bookeddate_str, '%Y-%m-%d').date()
        bookedStartTime = datetime.strptime(startTime_str, '%H:%M').time()
        bookedEndTime = datetime.strptime(endTime_str, '%H:%M').time()

        # print(bookedStartTime)
        # print(current_user.id)
        # basically if there is a post request take that student_id, tutor id and time slot and save it in session.
        #form = request.POST

        slot = Availability.objects.filter(tutor_id=tutorID)
        wallet = Wallet.objects.get(user=sid.user)

        currentDate = str(datetime.today().date())
        currentTime = str(datetime.now().hour) + ":" + \
            str(datetime.now().minute)
        syswallet = SystemWallet.objects.get()
        sessions = Sessions.objects.filter(tutorID=tutorID)
        print(sessions)

        try:
            Sessions_instance = Sessions.objects.create(
                tutorID=tutor, studentID=sid, bookedDate=bookedDate, bookedStartTime=bookedStartTime, bookedEndTime=bookedEndTime, sessionAmount=tutor.hourly_rate, systemWallet=syswallet)  # add the new session to the db table
            # selectedSlot.isAvailable = False  # make the slot unavailable
            # selectedSlot.save()  # save the slot
            sessionAmount = (float)(tutor.hourly_rate) + \
                (float)(tutor.hourly_rate) * (0.05)
            #wallet.amount -= sessionAmount
            # still stuff to do
            # print(balance)
            return HttpResponse('success')
            return render(request, 'main/home.html', {})
            # return HttpResponse("Your Session is Successfully Booked!")

        except ValidationError as e:
            return JsonResponse({'status': 'false', 'message': 'You have another session at the same time or already have a session with this tutor today!'}, status=500)
        return HttpResponse("Confirmed!")

    # if not slot:
    #     return HttpResponse('<em> Oops! This Tutor has no available time slots </em>')

    # else:
    #     if request.method == 'POST':
    #         selectedSlot = get_object_or_404(Availability, pk=request.POST.get(
    #             'slot_id'))  # get user's selected slot from the drop down
    #
    #
    # return render(request, self.template_name, {'slots': slot})


def tutorSchedule(request):

    current_user = request.user

    try:
        tutor = Tutor.objects.get(user=current_user)  # get tutor object
    except:
        raise Http404("Sorry! You are not registered as a Tutor!")

    slot = Availability.objects.filter(tutor=tutor)  # blocked slots
    # wallet = Wallet.objects.get(user=sid.user)
    currentDate = str(datetime.today().date())
    currentTime = str(datetime.now().hour) + ":" + str(datetime.now().minute)
    syswallet = SystemWallet.objects.get()
    sessions = Sessions.objects.filter(tutorID=tutor.id)

    return render(request, 'main/WelcomeTutor.html', {'slots': slot, 'tutor': tutor, 'currentDate': currentDate, 'currentTime': currentTime, 'sessions': sessions})


def blockSuccess(request):

    if request.method == 'POST':
        current_user = request.user
        tutor = Tutor.objects.get(user=current_user)  # get tutor object

        bookeddate_str = request.POST['blockeddate']
        startTime_str = request.POST['startTime']
        endTime_str = request.POST['endTime']
        decision = request.POST['decision']

        availDate = datetime.strptime(bookeddate_str, '%Y-%m-%d').date()
        availStartTime = datetime.strptime(startTime_str, '%H:%M').time()
        availEndTime = datetime.strptime(endTime_str, '%H:%M').time()
        print(availStartTime)
        if decision == "2":  # block

            try:
                Availability.objects.create(
                    tutor=tutor, date=availDate, startTime=availStartTime, endTime=availEndTime)
                print("created")
                return HttpResponse('success')

            except:
                print("Error")

        elif decision == "1":
            unblockSlot = Availability.objects.get(
                tutor=tutor, date=availDate, startTime=availStartTime, endTime=availEndTime)
            unblockSlot.delete()
            return HttpResponse('success')


@login_required
def mySessions(request):  # View your sessions and cancel them

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

        # If slot is less than 24 hours away dont allow to cancel
        if(slotToCancel.bookedDate == (datetime.now().date() + timedelta(days=1))):
            tomorrowSlot = timedelta(
                hours=slotToCancel.bookedStartTime.hour, minutes=slotToCancel.bookedStartTime.minute)
            nowSlot = timedelta(hours=datetime.today().time(
            ).hour, minutes=datetime.today().time().minute)

            if tomorrowSlot - nowSlot < timedelta(hours=24):
                return HttpResponse('<em> Sorry! You cannot cancel a session less than 24 hours before it is scheduled.</em>')

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
    wallet = Wallet.objects.get(user=currentUser)
    student = Student.objects.get(user=currentUser)

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
    transactionList = "Hi"

    return render(request, 'main/wallet.html', {'wallet': wallet, 'user': currentUser, 'sessions': transactionList, 'walletForm': walletForm})


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
