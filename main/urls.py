from django.conf.urls import url

from django.views.generic.detail import DetailView
from django.conf.urls.static import static
from main import views
from django.conf import settings
from django.conf.urls import include, url
# from main.admin import my_new_admin
from django.contrib import admin
from django.contrib.auth.views import (
   password_reset,
   password_reset_done,
   password_reset_confirm,
   password_reset_complete
)

app_name = 'main'

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^home/$', views.homePage, name='home-page'),
    url(r'^search/$', views.search, name='search'),
    url(r'^reset-password/$',password_reset, name = 'password_reset'),
    url(r'^reset-password/done/$',password_reset_done, name = 'password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',password_reset_confirm, name = 'password_reset_confirm'),
    url(r'^reset-password/complete/$',password_reset_complete, name = 'password_reset_complete'),
    url(r'^register/$', views.register, name='register'),
    url(r'^studentreg/$', views.studentRegistration, name='studentreg'),
    url(r'^tutorreg/$', views.register2, name='tutorreg'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^tutorWallet/$', views.tutorWallet, name='tutorWallet'),
    url(r'^studentWallet/$', views.studentWallet, name='studentWallet'),
    url(r'^myTutorsWallet/$', views.myTutorsWallet, name='myTutorsWallet'),
    url(r'^tutorSchedule/$', views.tutorSchedule, name='tutorSchedule'),
    url(r'^blockSuccess/$', views.blockSuccess, name='blockSuccess'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^tutor_login/$', views.user_login1, name='tutor_login'),
    url(r'^tutorhome/$', views.tutorHome, name='tutor_home'),
    url(r'^session/$', views.bookSession, name='session'),
    url(r'^confirmedBooking/$', views.confirmedBooking, name='confirmedBooking'),
    url(r'^mySessions/$', views.mySessions, name='mySessions'),
    url(r'^tutors$', views.TutorListView.as_view(), name='tutor-list'),
    url(r'^tutors/(?P<pk>\d+)$', views.TutorDetailView, name='tutor-detail'),
    url(r'^tutors/viewprofile/', views.TutorViewProfile, name='tutor-viewprofile'),
    url(r'^myTutors$', views.myTutorsHome, name='myTutors'),
    url(r'^tutors/update/(?P<pk>\d+)$', views.TutorUpdateView.as_view(), name='tutor-update'),
    url(r'^reviews$', views.review, name='review-list'),
    url(r'^reviews/(?P<pk>\d+)$', views.reviewForm, name='review-form'),
    url(r'^tutorMySessions$', views.tutorMySessions, name='tutorMySessions')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
