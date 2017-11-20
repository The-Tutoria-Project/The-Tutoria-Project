from django.core.management.base import BaseCommand
from main.models import Sessions, Tutor, SystemWallet, Transactions, Student
from django.contrib.sites.models import Site
from datetime import datetime, timedelta, time

class Command(BaseCommand):

    def handle(self, *args, **options):

        TUTORIA_COMMISSION = 0.05 # add this to systemWallet

        endedTime = time(11,30)
        endedSessions = Sessions.objects.filter(bookedEndTime = endedTime)
        print(endedSessions)

        sysWallet = Site.objects.get_current().systemwallet


        for slot in endedSessions:

            tutor = Tutor.objects.get(user=slot.tutorID.user)
            amountToPay = (float)(tutor.hourly_rate)

            sysWallet.systemBalance = (float)(sysWallet.systemBalance) - amountToPay
            sysWallet.save()

            tutor.wallet = (float)(tutor.wallet)+amountToPay
            tutor.save()

            Transactions.objects.create(user=tutor.user, transactionTime=datetime.now(), addedAmount=amountToPay, subtractedAmount=0, details='Received Payment for Session with '+str(slot.studentID.firstName)+" "+str(slot.studentID.lastName))


        #delete sessions and transactions > 30 days old
        deleteTransactions = Transactions.objects.filter(transactionTime__lt=(datetime.now().date() - timedelta(days=30)))
        deleteSessions = Sessions.objects.filter(bookedDate__lt=(datetime.now().date() - timedelta(days=30)))

        for transaction in deleteTransactions:
            transaction.delete()

        for session in deleteSessions:
            session.delete()
