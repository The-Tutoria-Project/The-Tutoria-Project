from django.core.management.base import BaseCommand
from main.models import Sessions, Tutor, Wallet, SystemWallet
from datetime import datetime, timedelta, time

class Command(BaseCommand):



    def handle(self, *args, **options):

        TUTORIA_COMMISSION = 0.05 # add this to systemWallet

        endedTime = time(11,30)
        endedSessions = Sessions.objects.filter(bookedTime__endTime = endedTime)
         #change line by adding admin to systemWallet user

        for slot in endedSessions:

            tutorWallet = Wallet.objects.get(user= slot.tutorID.user)
            amountToPay = (float)(slot.sessionAmount) - (float)(slot.sessionAmount)*TUTORIA_COMMISSION
            print(amountToPay)
            systemWallet = SystemWallet.objects.get(id= slot.systemWallet.id)
            systemWallet.systemBalance -= (int)(amountToPay) #change from int
            tutorWallet.amount += (int)(amountToPay)   #change from int
            systemWallet.save()
            tutorWallet.save()
