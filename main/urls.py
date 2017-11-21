from django.conf.urls import url

from django.views.generic.detail import DetailView
from django.conf.urls.static import static
from main import views
from django.conf import settings
from django.conf.urls import include, url
# from main.admin import my_new_admin
from django.contrib import admin


app_name = 'main'

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^home/$', views.homePage, name='home-page'),
    url(r'^search/$', views.search, name='search'),
    # url(r'^my_new_admin/(*.)', my_new_admin.root),
    url(r'^register/$', views.register, name='register'),
    url(r'^studentreg/$', views.studentRegistration, name='studentreg'),
    url(r'^tutorreg/$', views.register2, name='tutorreg'),
    #url(r'^studentandtutreg/$', views.register3, name='tutorreg'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^tutorWallet/$', views.tutorWallet, name='tutorWallet'),
    url(r'^studentWallet/$', views.studentWallet, name='studentWallet'),
    # url(r'^studentRegistration/$', views.studentRegistration, name='studentRegistration'),
    # url(r'^account/', include('django.contrib.auth.urls')),

    url(r'^tutorSchedule/$', views.tutorSchedule, name='tutorSchedule'),
    url(r'^blockSuccess/$', views.blockSuccess, name='blockSuccess'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^tutor_login/$', views.user_login1, name='tutor_login'),
    url(r'^confirmedBooking/$', views.confirmedBooking, name='confirmedBooking'),
    url(r'^session/$', views.bookSession, name='session'),
    url(r'^mySessions/$', views.mySessions, name='mySessions'),
    url(r'^tutors$', views.TutorListView.as_view(), name='tutor-list'),
    url(r'^tutors/(?P<pk>\d+)$', views.TutorDetailView, name='tutor-detail'),
    url(r'^tutors/update/(?P<pk>\d+)$', views.TutorUpdateView.as_view(), name='tutor-update'),
    url(r'^reviews$', views.review, name='review-list'),
    url(r'^reviews/(?P<pk>\d+)$', views.reviewForm, name='review-form'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
