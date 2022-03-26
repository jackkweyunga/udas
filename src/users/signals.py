from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from systemlogging.models import SystemLogs

@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    
    if created:
        log = SystemLogs(
            log_content=f"user {instance.email} was created",
            model_logged = "user",
        )
        log.save()
        print(sender)


# more signals needed