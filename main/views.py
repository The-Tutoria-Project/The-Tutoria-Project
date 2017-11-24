import json

from . import models
from main.forms import UserForm, StudentInfoForm, BookingForm, TutorInfoForm

#Searching
from django.db.models import Q
from django.db.models import Max
from decimal import Decimal as D

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response, redirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic import View, ListView, DetailView, TemplateView, UpdateView

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from main.models import Availability, Sessions, Student, Tutor, Course, SystemWallet, Transactions, Review
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.http import JsonResponse, Http404
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime, timedelta
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail

class IndexView(TemplateView):
    template_name = 'index.html'


def signup(request):
    return render(request, 'signup.html', {})


def change_password(request):

    if request.method == "POST":
        form = PasswordChangeForm(data = request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('/main/home')
        else:
            return redirect('/main/change_password')


    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'main/change_password.html',args)

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

            Student.user = request.user
            Student.email = request.user.email
            print(request.FILES)
            if 'avatar' in request.FILES:
                Student.avatar = request.FILES['avatar']

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
            tutorInst.tutor_email = request.user.email

            if 'avatar' in request.FILES:
                Tutor.avatar = request.FILES['avatar']

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
                return redirect('/main/home/')
                # return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT INACTIVE")
        else:
            print("Login failed")
            return HttpResponse("Invalid login details")


    return render(request, 'main/login.html', {})



def user_login1(request):  # For Tutor
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                try:
                    Tutor.objects.get(user=user)
                    login(request, user)
                    return redirect('/main/tutorhome/')
                    # return HttpResponseRedirect(reverse('index'))

                except:
                    return HttpResponse("Sorry! You are not registered as a Tutor!")

            else:
                return HttpResponse("ACCOUNT INACTIVE")
        else:
            print("Login failed")
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'main/login1.html', {})

def tutorHome(request):
    return render(request, 'main/tutor_home.html', {})


def myTutorsHome(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active and user.is_staff:
                return redirect('/main/myTutorsWallet/')

    return render(request, 'main/loginMyTutors.html', {})

def myTutorsWallet(request):

    currentUser=request.user
    sysWallet = Site.objects.get_current().systemwallet

    if request.method == 'POST':

        amount = 0
        amountstr = request.POST.get("amount")

        try:
            amount = (float)(amountstr)
        except:
            amount = 0

        if (float)(sysWallet.systemBalance) > amount:
            sysWallet.systemBalance = (float)(sysWallet.systemBalance) - amount
            sysWallet.save()
            return render(request,'main/myTutorsWallet.html', {'user': request.user, 'wallet': sysWallet})


    return render(request, 'main/myTutorsWallet.html', {'user': request.user, 'wallet': sysWallet})


class TutorListView(ListView):

    context_object_name = 'tutors'
    model = models.Tutor

@login_required
def TutorDetailView(request, pk):

    tutor = get_object_or_404(Tutor, id=pk)
    review = Review.objects.filter(session__tutorID=tutor, submitted=True)
    reviewCount = Review.objects.filter(session__tutorID=tutor, submitted=True).count()
    print(review)
    return render(request, 'main/tutor_detail.html', {'tutor_details': tutor, 'reviews':review, 'reviewCount':reviewCount})

@login_required
def TutorViewProfile(request):

    try:
        tutor = Tutor.objects.get(user=request.user)
    except:
        return HttpResponse("Sorry! You are not registered as a Tutor!")

    review = Review.objects.filter(session__tutorID=tutor, submitted=True)
    # reviewCount = Review.objects.filter(session__tutorID=tutor, submitted=True).count()
    return render(request, 'main/tutor_viewprofile.html', {'tutor': tutor, 'reviews':review })

class TutorUpdateView(UpdateView):
    fields = ('tutor_email','avatar','phoneNo','university_name','courses','tutor_intro','hourly_rate','isActive','searchTags')
    model = models.Tutor



def bookSession(request):

    current_user = request.user
    try:
        student = Student.objects.get(user=current_user)  # student
    except:
        return HttpResponse("Sorry! You are not registered as a Student!")

    tutorID = request.GET["value1"]
    tutor = Tutor.objects.get(id=tutorID)  # get tutor object

    slot = Availability.objects.filter(tutor_id=tutorID)  # blocked slots

    currentDate = str(datetime.today().date())
    currentTime = str(datetime.now().hour) + ":" + str(datetime.now().minute)

    sessions = Sessions.objects.filter(tutorID=tutorID)

    return render(request, 'main/session.html', {'slots': slot, 'tutor': tutor, 'balance': student, 'currentDate': currentDate, 'currentTime': currentTime, 'sessions': sessions})



def confirmedBooking(request):

    if request.method == 'POST':
        current_user = request.user
        tutorID = request.POST['tutID']
        tutor = Tutor.objects.get(id=tutorID)
        student = Student.objects.get(user=current_user)

        slot = Availability.objects.filter(tutor_id=tutorID)
        currentDate = str(datetime.today().date())
        currentTime = str(datetime.now().hour) + ":" + \
            str(datetime.now().minute)
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
        # form = request.POST

        slot = Availability.objects.filter(tutor_id=tutorID)

        currentDate = str(datetime.today().date())
        currentTime = str(datetime.now().hour) + ":" + \
            str(datetime.now().minute)

        sysWallet = Site.objects.get_current().systemwallet
        sessionAmount = (float)(tutor.hourly_rate) * \
            (1 + sysWallet.TUTORIA_COMMISSION)

        try:
            if((float)(student.wallet) - sessionAmount >= 0):
                Sessions_instance = Sessions.objects.create(
                    tutorID=tutor, studentID=student, bookedDate=bookedDate, bookedStartTime=bookedStartTime, bookedEndTime=bookedEndTime, sessionAmount=tutor.hourly_rate)  # add the new session to the db table
                sysWallet.systemBalance = (float)(
                    sysWallet.systemBalance) + sessionAmount
                sysWallet.save()
                student.wallet = (float)(student.wallet) - sessionAmount
                student.save()

                transaction = Transactions.objects.create(user=student.user, transactionTime=datetime.now(
                ), addedAmount=0, subtractedAmount=sessionAmount, details="Booked a " + str(Sessions_instance))


                send_mail(
                'Tutoria: You have been Booked for a new Session!',
                "Dear " + tutor.firstName + ", You have been booked by " + student.firstName + "  for a session on " + str(Sessions_instance.bookedDate) + " from " + str(Sessions_instance.bookedStartTime) + " to " + str(Sessions_instance.bookedEndTime),
                'myTutors@gmail.com',
                [tutor.tutor_email],
                fail_silently=False,
                )

                send_mail(
                'Tutoria: You have Booked a new Session!',
                "The details of your upcoming session are: " + str(Sessions_instance),
                'myTutors@gmail.com',
                [student.email],
                fail_silently=False,
                )


            else:
                print("error")
                return HttpResponse("You dont have enough money for this :(")
                # selectedSlot.isAvailable = False  # make the slot unavailable
            # selectedSlot.save()  # save the slot
            # wallet.amount -= sessionAmount
            # still stuff to do
            # print(balance)

            return HttpResponse('success')

            # return HttpResponse("Your Session is Successfully Booked!")

        except:
            return HttpResponse('error')
        # except ValidationError as e:
        #     return JsonResponse({'status': 'false', 'message': 'You have another session at the same time or already have a session with this tutor today!'}, status=500)
        # return HttpResponse("Confirmed!")

    # if not slot:
    #     return HttpResponse('<em> Oops! This Tutor has no available time slots </em>')

    # else:
    #     if request.method == 'POST':
    #         selectedSlot = get_object_or_404(Availability, pk=request.POST.get(
    #             'slot_id'))  # get user's selected slot from the drop down
    #
    #
    # return render(request, self.template_name, {'slots': slot})

@login_required
def tutorSchedule(request):

    current_user = request.user

    try:
        tutor = Tutor.objects.get(user=current_user)  # get tutor object
    except:
        raise Http404("Sorry! You are not registered as a Tutor!")

    slot = Availability.objects.filter(tutor=tutor)  # blocked slots
    # wallet = Wallet.objects.get(user=student.user)
    currentDate = str(datetime.today().date())
    currentTime = str(datetime.now().hour) + ":" + str(datetime.now().minute)
    syswallet = SystemWallet.objects.get()
    sessions = Sessions.objects.filter(tutorID=tutor.id)

    return render(request, 'main/WelcomeTutor.html', {'slots': slot, 'tutor': tutor, 'currentDate': currentDate, 'currentTime': currentTime, 'sessions': sessions})

@login_required
def blockSuccess(request):

    if request.method == 'POST':
        current_user = request.user
        try:
            tutor = Tutor.objects.get(user=current_user)  # get tutor object
        except:
            raise Http404("Sorry! You are not registered as a Tutor!")

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

    try:
        student = Student.objects.get(user=currentStudent)
    except:
        raise Http404("Sorry! You are not registered as a Student!")

    bookedSlots = Sessions.objects.filter(studentID_id=student.id)
    sysWallet = Site.objects.get_current().systemwallet

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
                return render(request, 'main/mySessions.html', {'bookedSlots': bookedSlots, 'message': "Sorry! You cannot cancel a session less than 24 hours before it is scheduled"})
        # refund
        refundAmount = (float)(slotToCancel.tutorID.hourly_rate) * (1.0 + (sysWallet.TUTORIA_COMMISSION))

        # deduct from system
        sysWallet.systemBalance = (float)(
            sysWallet.systemBalance) - refundAmount
        sysWallet.save()

        # give to student
        student.wallet = (float)(student.wallet) + refundAmount
        student.save()

        # make session available by deleting it
        Transactions.objects.create(user=currentStudent, transactionTime=datetime.now(), addedAmount=refundAmount, subtractedAmount=0, details='Cancelled a '+str(slotToCancel))

        slotToCancel.delete()



        message = "Your slot has been successfully deleted. An amount of HKD " + str(refundAmount) + " has been refunded to your wallet"
        bookedSlots = Sessions.objects.filter(studentID_id=student.id)
        return render(request, 'main/mySessions.html', {'bookedSlots': bookedSlots, 'message': message})
    return render(request, 'main/mySessions.html', {'bookedSlots': bookedSlots})

def tutorMySessions(request):

    sessions = Sessions.objects.filter(tutorID__user=request.user)
    print(sessions)
    return render(request, 'main/tutorMySessions.html', {'bookedSlots': sessions} )



def homePage(request):
    return render(request, 'main/home.html')


# def studentreg(request):
#     return render(request, 'main/studentreg.html')

@login_required
def search(request):

    try:
        student = Student.objects.get(user=request.user)
    except:
        raise Http404("Sorry! You are not registered as a Student!")

    search = Tutor.objects.exclude(user=request.user).exclude(isActive=False)
    print(search)

    if request.method == 'GET':
        userName = request.GET.get('search_name')
        userUni=request.GET.get('search_uni')
        userC=request.GET.get('search_c')
        userS=request.GET.get('search_st')
        ttyp=request.GET.get('TutorType')
        search_7days = request.GET.get('search_7days')
        sortPrice = request.GET.get('sort_price')


        price1 = request.GET.get('min_price')
        price2 = request.GET.get('max_price')

        if price1 is None or price1 == '':
            price1=0

        else:
            price1 = (float)(price1)


        if price2 is None or price2 == '':

            price2 = Tutor.objects.all().aggregate(Max('hourly_rate'))  #setting max default rate incase field left blank
            price2 = price2['hourly_rate__max']

        else:
            price2 = (float)(price2)

         #should not display tutor if student and tutor are the same user

        try:
            if(ttyp=='2'): #

                search=Tutor.objects.filter((Q(firstName__startswith=userName) | Q(lastName__startswith=userName)), university_name__startswith=userUni,courses__name__startswith=userC,hourly_rate__lte=price2,hourly_rate__gte=price1, searchTags__icontains=userS).exclude(isActive=False).distinct()
                search = search.exclude(user = request.user)
                next7days = datetime.now().date() + timedelta(days=8)
                tomorrow = datetime.now().date() + timedelta(days=1)

                if search_7days == 'on':
                    for tutor in search:
                        booked = Sessions.objects.filter(tutorID=tutor, bookedDate__range=(tomorrow,next7days)).count()
                        blocked = Availability.objects.filter(tutor=tutor, date__range=(tomorrow,next7days)).count()

                        print(booked+blocked)

                        if (booked+blocked) >= 56: #max 56 slots for private tutor in 7 days
                            print(booked+blocked)
                            print("exclude")
                            search = search.exclude(pk=tutor.pk)

                # if userS is not None or userS != '':
                #     for tutor in search:
                #         tag_list = tutor.searchTags.split()
                #         print(tag_list)


                if sortPrice == 'on':
                   search = search.order_by('hourly_rate')

                    #print("THIS IS THE COUNT" + str(booked+blocked))
            else:
                search=Tutor.objects.filter((Q(firstName__startswith=userName) | Q(lastName__startswith=userName)), university_name__startswith=userUni,courses__name__startswith=userC,tutorType=ttyp,hourly_rate__lte=price2,hourly_rate__gte=price1, searchTags__icontains=userS).exclude(isActive=False).distinct()
                search = search.exclude(user = request.user)
                next7days = datetime.now().date() + timedelta(days=8)
                tomorrow = datetime.now().date() + timedelta(days=1)

                if search_7days == 'on':
                    for tutor in search:
                        booked = Sessions.objects.filter(tutorID=tutor, bookedDate__range=(tomorrow,next7days)).count()
                        blocked = Availability.objects.filter(tutor=tutor, date__range=(tomorrow,next7days)).count()

                        maxSlots = 56
                        if tutor.tutorType == 0:
                            maxSlots = 112

                        if (booked+blocked) >= maxSlots: #max 56 slots for private tutor in 7 days
                            print(booked+blocked)
                            print("exclude")
                            search = search.exclude(pk=tutor.pk)

                if sortPrice == 'on':
                   search = search.order_by('hourly_rate')


            return render(request, 'main/search.html', {'tutors': search})

        except:
            print("except")
            return render(request, 'main/search.html', {'tutors': search})

    return render(request, 'main/search.html', {'tutors': search})

@login_required
def review(request):

    currentUser = request.user
    student = get_object_or_404(Student, user=currentUser)
    review = Review.objects.filter(session__studentID__user=request.user, submitted=False)

    if request.method == 'POST':
        reviewID = request.POST['id']
        Review.objects.get(id=reviewID).delete()
        return render(request, 'main/review_list.html', {'review_list': review})



    return render(request, 'main/review_list.html', {'review_list': review})

@login_required
def reviewForm(request, pk):


    review = get_object_or_404(Review, id=pk)
    print(pk)
    print(review)
    tutor = Tutor.objects.get(id=review.session.tutorID.id)

    if request.method == 'POST':



        try:
            comments = request.POST.get('comments')
            rating = (float)( request.POST.get('rating') )
            check = request.POST.get('check_anon', False)
            review.rating = rating
            review.comments = comments
            review.submitted = True
            if str(check) == "False":
                review.isAnonymous = False
            else:
                review.isAnonymous = True

            tutor.numReviews = tutor.numReviews + 1

            allreviews = tutor.numReviews
            review.save()

            tutor.averageRating = ( (float)(tutor.averageRating*(allreviews-1))+ (float)(review.rating))/ (float)(allreviews);
            tutor.save()

            return render(request, 'main/home.html')


        except:
            print('hey bro')
            message = "Invalid Submission"
            return render(request, 'main/reviewForm.html', {'tutor': tutor, 'message':message})


    return render(request, 'main/reviewForm.html', {'tutor': tutor})

@login_required
def tutorWallet(request):

    currentUser=request.user
    tutor=get_object_or_404(Tutor, user = currentUser)
    #transaction for 30 days only
    transactionList=Transactions.objects.filter(user = currentUser).exclude(transactionTime__lt=(datetime.now().date() - timedelta(days=30)))
    print(transactionList)


    if request.method == 'POST':
        amountstr=request.POST.get("amount")

        try:
            amount = (float)(amountstr)
        except:
            amount = 0
            return render(request, 'main/tutorWallet.html', {'tutor': tutor, 'transactions': transactionList, 'message': "Please enter a valid amount"})

        tutor.wallet=(float)(tutor.wallet) - amount
        try:
            tutor.save()

            Transactions.objects.create(user=currentUser, transactionTime=datetime.now(), addedAmount=0, subtractedAmount=amount, details='Transferred money from wallet')

            successmsg='Successfully transferred HKD ' + amountstr + " from your wallet!"
            return render(request, 'main/tutorWallet.html', {'tutor': tutor, 'transactions': transactionList, 'message': successmsg})

        except:
            raise Http404("Oops! Could not add money. Please try again.")

    return render(request, 'main/tutorWallet.html', {'tutor': tutor, 'transactions': transactionList})

@login_required
def studentWallet(request):

    currentUser=request.user
    student=get_object_or_404(Student, user = currentUser)
    transactionList=Transactions.objects.filter(user = currentUser).exclude(transactionTime__lt=(datetime.now().date() - timedelta(days=30)))

    if request.method == 'POST':
        amountstr=request.POST.get("amount")
        print("neeche dekh")
        print(amountstr)
        print("del")

        try:
            amount=(float)(amountstr)

        except:
            successmsg = "Please enter a valid amount"
            return render(request, 'main/studentWallet.html', {'student': student, 'transactions': transactionList, 'message': successmsg})



        student.wallet=(float)(student.wallet) + amount
        try:
            student.save()

            Transactions.objects.create(user=currentUser, transactionTime=datetime.now(), addedAmount=amount, subtractedAmount=0, details='Added money to wallet')

            successmsg='Successfully added HKD ' + amountstr + " to your wallet!"
            return render(request, 'main/studentWallet.html', {'student': student, 'transactions': transactionList, 'message': successmsg})

        except:
            raise Http404("Oops! Could not add money. Please try again.")

    return render(request, 'main/studentWallet.html', {'student': student, 'transactions': transactionList})

    # wallet = Wallet.objects.get(user=currentUser)
    # student = Student.objects.get(user=currentUser)
    #
    # #if request.method == "POST":
    #
    #     #walletForm = AddToWallet(data=request.POST)
    #
    #     #if walletForm.is_valid():
    #
    #     #    wallet.amount += walletForm.cleaned_data['amount']
    #     #    wallet.save()
    #
    #     #else:
    #     #    print(walletForm.errors)
    #
    # #else:
    #     #walletForm = AddToWallet()
    #
    # tminus30days = datetime.today() - timedelta(days=30)
    # transactionList = "Hi"
    #
    # return render(request, 'main/wallet.html', {'wallet': wallet, 'user': currentUser, 'sessions': transactionList, 'walletForm': walletForm})
