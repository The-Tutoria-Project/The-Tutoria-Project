from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
import uuid
import datetime
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse



# class Transactions
class Course(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name


class SearchTag(models.Model):
    tagName = models.CharField(max_length=128)

    def __str__(self):
        return self.tagName

class SystemWallet(models.Model):
    systemBalance = models.DecimalField(max_digits=10, decimal_places=2)

# Create your models here.
class Tutor(models.Model):

    user = models.OneToOneField(User)

    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    tutor_email = models.EmailField(max_length=254, unique=True)
    university_name = models.CharField(max_length=200)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    tutor_intro = models.TextField()
    avatar = models.ImageField(upload_to='profile_pics', blank=True)

    TUTOR_TYPE = (
        (0, 'Contracted'),
        (1, 'Private'),
    )
    tutorType = models.PositiveSmallIntegerField(choices=TUTOR_TYPE, default=0)

    courses = models.ManyToManyField(Course)
    searchTags = models.ManyToManyField(SearchTag)
    tutor_booking_status = models.BooleanField()


    def __str__(self):
        return self.firstName + " " + self.lastName

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        # return reverse('tutor-detail-view', args=[str(self.id)])
        return reverse("main:tutor-detail", kwargs={'pk':self.pk})

    # def time_slots(self):
    #     return ', '.join([a.start_time for a in self.available_time.all()])


class Availability(models.Model): #blocked slots

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
    isAvailable = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Availabilities"
        # unique_together = (("tutor", "weekday", "startTime"), ("tutor",
        #                                                        "weekday", "endTime"), ("tutor", "weekday", "startTime", "endTime"))

    def __str__(self):
        # return str(self.weekday) + " " + str(self.start_time) + "-" + str(self.end_time)
        #return str(self.get_month_display()) + " " + str(self.get_day_display()) + ", " + str(self.tutor) + " " + str(self.startTime) + " - " + str(self.endTime)
        return str(self.tutor) + " " + str(self.date) + " " + str(self.startTime) + " - " + str(self.endTime)


class Student(models.Model):
    user = models.OneToOneField(User)
    #student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    email = models.EmailField(max_length=254, unique=True)
    wallet = models.DecimalField(max_digits=8, decimal_places=2, default=1000)
    #student_booking_status = models.BooleanField()
    #tutor = models.ForeigKey(Tutor)

    def __str__(self):
        return self.firstName


class Sessions(models.Model):

    studentID = models.ForeignKey(Student)
    tutorID = models.ForeignKey(Tutor)
    bookedTime = models.ForeignKey(
        Availability, related_name='sessionKey', null=True)
    sessionAmount = models.DecimalField(max_digits=8, decimal_places=2)
    systemWallet = models.ForeignKey(SystemWallet)

    def __str__(self):
        return self.studentID.firstName + " " + str(self.bookedTime.startTime) + " " + self.tutorID.firstName

    class Meta:
        verbose_name_plural = "Sessions"
        unique_together = (("studentID", "tutorID", "bookedTime"))

    def validate_unique(self, exclude=None):
        check = Sessions.objects.filter(studentID=self.studentID)

        # Student cannot book a session starting at same time
        if check.filter(bookedTime__startTime=self.bookedTime.startTime).exists():
            raise ValidationError('Another session starting at same time')

        # Student cannot book a session ending at same time
        if check.filter(bookedTime__endTime=self.bookedTime.endTime).exists():
            raise ValidationError('Another session ending at same time')

        # if check.filter(bookedTime__weekday=self.bookedTime.weekday).exists() and check.filter(tutorID=self.tutorID).exists(): #Student cannot book a session ending at same time
        #     raise ValidationError('Already one session with this tutor today')

    def save(self, *args, **kwargs):

        self.validate_unique()

        super(Sessions, self).save(*args, **kwargs)


class Wallet(models.Model):
    user = models.OneToOneField(User)
    currency = models.CharField(max_length=3, default="HKD")
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.user)

class Review(models.Model):
    student = models.ForeignKey(Student)
    tutor = models.ForeignKey(Tutor)
    rating = models.DecimalField(max_digits=6, decimal_places=1)
    comments = models.CharField(max_length = 256)

class Coupon(models.Model):
    couponCode = models.CharField(max_length=6, default="000000")
    expiryDate = models.DateField()



#
# class Booking(model.Model):
#
#     tutor_id = models.ForeignKey(Tutor)
#     student_id = models.ForeignKey(Student)
#     session = models.ForeignKey(Availability)
