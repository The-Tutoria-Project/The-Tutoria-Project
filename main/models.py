from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
import uuid
import datetime
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


# class Transactions
class Course(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name


class SearchTag(models.Model):
    tagName = models.CharField(max_length=128)

    def __str__(self):
        return self.tagName


# tied to the django site
class SystemWallet(models.Model):
    TUTORIA_COMMISSION = 0.05
    site = models.OneToOneField(Site)
    systemBalance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "MyTutors System Wallet"




class Tutor(models.Model):

    user = models.OneToOneField(User)
    isStudent = models.BooleanField(default=True)
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    tutor_email = models.EmailField(max_length=254, unique=True)
    university_name = models.CharField(max_length=200)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    tutor_intro = models.TextField()
    wallet = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0.1)])
    avatar = models.ImageField(upload_to='profile_pics', blank=True)

    TUTOR_TYPE = (
        (0, 'Contracted'),
        (1, 'Private'),
    )
    tutorType = models.PositiveSmallIntegerField(choices=TUTOR_TYPE, default=0)

    courses = models.ManyToManyField(Course)
    searchTags = models.ManyToManyField(SearchTag)
    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # tutor_booking_status = models.BooleanField()

    def __str__(self):
        return self.firstName + " " + self.lastName

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        # return reverse('tutor-detail-view', args=[str(self.id)])
        return reverse("main:tutor-detail", kwargs={'pk': self.pk})

    # def time_slots(self):
    #     return ', '.join([a.start_time for a in self.available_time.all()])


class Availability(models.Model):  # blocked slots

    tutor = models.ForeignKey(Tutor, null=True)
    date = models.DateField()
    # MONTH_CHOICES = (
    #     (0, 'Jan'),
    #     (1, 'Feb'),
    #     (2, 'Mar'),
    #     (3, 'Apr'),
    #     (4, 'May'),
    #     (5, 'Jun'),
    #     (6, 'Jul'),
    #     (7, 'Aug'),
    #     (8, 'Sep'),
    #     (9, 'Oct'),
    #     (10, 'Nov'),
    #     (11, 'Dec'),
    # )
    #
    # DAY_CHOICES = ()
    # for i in range(0, 32):
    #     DAY_CHOICES += ((i, str(i + 1)),)
    #
    # WEEKDAY_CHOICES = (
    #     (0, 'Monday'),
    #     (1, 'Tuesday'),
    #     (2, 'Wednesday'),
    #     (3, 'Thursday'),
    #     (4, 'Friday'),
    #     (5, 'Saturday'),
    #     (6, 'Sunday'),
    # )
    # # Tutor.objects.values_list('available_time__weekday')
    # month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES)
    # day = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    # weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)
    startTime = models.TimeField()
    endTime = models.TimeField()

    class Meta:
        verbose_name_plural = "Availabilities"
        unique_together = ("tutor", "date", "startTime", "endTime")
        # unique_together = (("tutor", "weekday", "startTime"), ("tutor",
        #                                                        "weekday", "endTime"), ("tutor", "weekday", "startTime", "endTime"))

    def __str__(self):
        # return str(self.weekday) + " " + str(self.start_time) + "-" + str(self.end_time)
        # return str(self.get_month_display()) + " " + str(self.get_day_display()) + ", " + str(self.tutor) + " " + str(self.startTime) + " - " + str(self.endTime)
        return str(self.tutor) + " " + str(self.date) + " " + str(self.startTime) + " - " + str(self.endTime)


class Student(models.Model):
    user = models.OneToOneField(User)
    # student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    email = models.EmailField(max_length=254, unique=True)
    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # student_booking_status = models.BooleanField()
    # tutor = models.ForeigKey(Tutor)

    def __str__(self):
        return self.firstName


class Sessions(models.Model):

    studentID = models.ForeignKey(Student)
    tutorID = models.ForeignKey(Tutor)
    bookedDate = models.DateField(null=True)
    bookedStartTime = models.TimeField(null=True)
    bookedEndTime = models.TimeField(null=True)
    sessionAmount = models.DecimalField(max_digits=8, decimal_places=2)
    #systemWallet = models.ForeignKey(SystemWallet)

    def __str__(self):
        return "Session with " + self.tutorID.firstName + " on " + str(self.bookedDate) + " " + str(self.bookedStartTime) + " - " + str(self.bookedEndTime) + " for " + self.studentID.firstName

    class Meta:
        verbose_name_plural = "Sessions"
        unique_together = (
            (("studentID", "tutorID", "bookedDate"), ("studentID",
                                                      "tutorID", "bookedDate", "bookedStartTime", "bookedEndTime"))
        )

    def validate_unique(self, exclude=None):
        check = Sessions.objects.filter(studentID=self.studentID)

    def save(self, *args, **kwargs):

        self.validate_unique()

        super(Sessions, self).save(*args, **kwargs)


class Transactions(models.Model):
    user = models.ForeignKey(User)
    transactionTime = models.DateTimeField()
    addedAmount = models.DecimalField(max_digits=8, decimal_places=2)
    subtractedAmount = models.DecimalField(max_digits=8, decimal_places=2)
    details = models.CharField(max_length=256)

    def __str__(self):
        return str(self.user)


class Review(models.Model):

    session = models.OneToOneField(Sessions, null=True)
    rating = models.DecimalField(max_digits=6, decimal_places=1, null=True)
    comments = models.CharField(max_length=256, null=True)
    submitted = models.BooleanField(default=False, null=False)




class Coupon(models.Model):
    couponCode = models.CharField(max_length=6, default="000000")
    expiryDate = models.DateField()


#
# class Booking(model.Model):
#
#     tutor_id = models.ForeignKey(Tutor)
#     student_id = models.ForeignKey(Student)
#     session = models.ForeignKey(Availability)
