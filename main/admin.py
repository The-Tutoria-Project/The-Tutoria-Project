from django.contrib import admin
from .models import User, Tutor, Student, Availability, Sessions, Course, Review, Coupon, SystemWallet, SearchTag, Transactions
from django.contrib.admin.sites import AdminSite
# from main.admin import courseadmin
from The_Tutoria_Project.admin import courseadmin

# Register your models here.
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Availability)
admin.site.register(Sessions)
admin.site.register(Review)
admin.site.register(Course)
admin.site.register(Coupon)
admin.site.register(SystemWallet)
admin.site.register(SearchTag)
admin.site.register(Transactions)

class CourseAdmin(admin.ModelAdmin):
    list_diplay = ['name']

courseadmin.register(Course, CourseAdmin)
