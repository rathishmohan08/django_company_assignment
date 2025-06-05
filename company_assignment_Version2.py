#question 1 
#answer :Yes. By default, Django signals are executed synchronously, meaning they block further execution until finished.
#code:
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import time

@receiver(post_save, sender=User)
def handle_user_save(sender, instance, **kwargs):
    print("Signal handler started...")
    time.sleep(3)  
    print("Signal handler finished.")

# views.py
from django.http import HttpResponse
from django.contrib.auth.models import User

def create_user_view(request):
    print("Before creating user")
    User.objects.create(username="rathish")
    print("After creating user")
    return HttpResponse("User creation complete")
    

#######################################################################################

#question 2 
#answer :Yes. Django signals by default run in the same thread as the caller
#code:
#signals.py
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def thread_checker(sender, instance, **kwargs):
    print("Signal thread ID:", threading.get_ident())

# views.py
import threading
from django.http import HttpResponse
from django.contrib.auth.models import User

def test_thread_view(request):
    print("View thread ID:", threading.get_ident())
    User.objects.create(username="thread_test")
    return HttpResponse("Thread test done")

#####################################################################################

#question 3
#answer :Yes. Django signals run within the same database transaction by default. You can hook into it using transaction.on_commit.
#code :
# signals.py
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def check_transaction(sender, instance, **kwargs):
    transaction.on_commit(lambda: print("Signal called after DB transaction is committed"))

# views.py
from django.db import transaction
from django.contrib.auth.models import User
from django.http import HttpResponse

def db_transaction_view(request):
    with transaction.atomic():
        User.objects.create(username="txn_test")
        print("Inside atomic transaction")
    return HttpResponse("Transaction done")

###########################################################################################