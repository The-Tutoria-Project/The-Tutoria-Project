from django.core.management.base import BaseCommand
from main.models import Sessions, Tutor, SystemWallet, Transactions, Student, Review
from django.contrib.sites.models import Site
from datetime import datetime, timedelta, time
from django.core.mail import send_mail

class Command(BaseCommand):

    def handle(self, *args, **options):

        TUTORIA_COMMISSION = 0.05 # add this to systemWallet

        endedTime = time(11,30)
        endedSessions = Sessions.objects.filter(bookedEndTime = endedTime)
        print(endedSessions)

        sysWallet = Site.objects.get_current().systemwallet


        for slot in endedSessions:

            tutor = Tutor.objects.get(user=slot.tutorID.user)
            student = Student.objects.get(user=slot.studentID.user)

            amountToPay = (float)(tutor.hourly_rate)

            sysWallet.systemBalance = (float)(sysWallet.systemBalance) - amountToPay
            sysWallet.save()

            tutor.wallet = (float)(tutor.wallet)+amountToPay
            tutor.save()

            send_mail(
            'Tutoria: You have received a payment for your session!',
            'Dear '+tutor.firstName+", you have received a payment for your latest session with " + student.firstName,
            'sagarg95@gmail.com',
            ['a@b.com'],
            fail_silently=False,
            )

            Transactions.objects.create(user=tutor.user, transactionTime=datetime.now(), addedAmount=amountToPay, subtractedAmount=0, details='Received Payment for Session with '+str(slot.studentID.firstName)+" "+str(slot.studentID.lastName))

            #invitation to review
            send_mail(
            'Tutoria: Submit a Review!',
            'Dear '+student.firstName+", you may now submit a review for your latest session with " + tutor.firstName,
            'sagarg95@gmail.com',
            ['b@c.com'],
            fail_silently=False,
            )
            Review.objects.create(student=student, tutor=tutor, submitted=False)

        #delete sessions and transactions > 30 days old
        deleteTransactions = Transactions.objects.filter(transactionTime__lt=(datetime.now().date() - timedelta(days=30)))
        deleteSessions = Sessions.objects.filter(bookedDate__lt=(datetime.now().date() - timedelta(days=30)))


        for transaction in deleteTransactions:
            transaction.delete()

        for session in deleteSessions:
            session.delete()
