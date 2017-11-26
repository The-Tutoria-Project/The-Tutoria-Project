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
    hourly_rate = models.DecimalField(
        max_digits=8, decimal_places=2, default=0)
    tutor_intro = models.TextField()
    wallet = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0.1)])
    avatar = models.ImageField(
        upload_to='profile_pics', default='images/default_avatar.jpg')
    phoneNo = models.PositiveIntegerField(
        validators=[MaxValueValidator(99999999)])

    TUTOR_TYPE = (
        (0, 'Contracted'),
        (1, 'Private'),
    )
    tutorType = models.PositiveSmallIntegerField(choices=TUTOR_TYPE, default=0)

    courses = models.ManyToManyField(Course)
    #searchTags = models.ManyToManyField(SearchTag)
    searchTags = models.CharField(max_length=256, default="Java")
    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    isActive = models.BooleanField(default=True)
    averageRating = models.DecimalField(
        max_digits=2, decimal_places=1, default=0)
    numReviews = models.PositiveIntegerField(default=0)
    # tutor_booking_status = models.BooleanField()

    def __str__(self):
        return self.firstName + " " + self.lastName

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        # return reverse('tutor-detail-view', args=[str(self.id)])
        return reverse("main:tutor-viewprofile")

    def clean(self):
        if self.hourly_rate % 10 != 0:
            raise ValidationError('Hourly rate can only be multiples of 10.')

        if self.tutorType == 0 and self.hourly_rate != 0:
            raise ValidationError(
                'Contracted Tutors may not enter hourly rate.')

    # def time_slots(self):
    #     return ', '.join([a.start_time for a in self.available_time.all()])


class Availability(models.Model):  # blocked slots

    tutor = models.ForeignKey(Tutor, null=True)
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()

    class Meta:
        verbose_name_plural = "Availabilities"
        unique_together = ("tutor", "date", "startTime", "endTime")
        # unique_together = (("tutor", "weekday", "startTime"), ("tutor",
        #                                                        "weekday", "endTime"), ("tutor", "weekday", "startTime", "endTime"))

    def __str__(self):

        return str(self.tutor) + " " + str(self.date) + " " + str(self.startTime) + " - " + str(self.endTime)


class Student(models.Model):
    user = models.OneToOneField(User)
    # student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    email = models.EmailField(max_length=254, unique=True)
    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    phoneNo = models.PositiveIntegerField(
        validators=[MaxValueValidator(99999999)])
    avatar = models.ImageField(
        upload_to='profile_pics', blank=True, default="images/default_avatar.jpg")

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
    isAnonymous = models.BooleanField(default=False)


class Coupon(models.Model):
    couponCode = models.CharField(max_length=6, default="000000")
    expiryDate = models.DateField()
