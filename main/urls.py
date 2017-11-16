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

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^wallet/$', views.myWallet, name='wallet'),
    # url(r'^studentRegistration/$', views.studentRegistration, name='studentRegistration'),
    # url(r'^account/', include('django.contrib.auth.urls')),


    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^session/$', views.bookSession, name='session'),
    url(r'^mySessions/$', views.mySessions, name='mySessions'),
    url(r'^tutors$', views.TutorListView.as_view(), name='tutor-list'),
    url(r'^tutors/(?P<pk>\d+)$', views.TutorDetailView.as_view(), name='tutor-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
