
from django.contrib.admin import AdminSite




class CourseAdminSite(AdminSite):
    site_header = 'Course Admin'

courseadmin = CourseAdminSite(name = 'courseadmin')
