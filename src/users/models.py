
from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.management.utils import get_random_secret_key

from django.core.management.utils import get_random_secret_key
            

class User(AbstractUser):

    """
        A custom user model
    """

    username = None
    phone = models.CharField(max_length=250, null=True, blank=True)

    email = models.EmailField(unique=True, db_index=True)
    secret_key = models.CharField(max_length=255, default=get_random_secret_key)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        swappable = 'AUTH_USER_MODEL'

    @property
    def name(self):
        """
            Returns a full name
        """
        if not self.last_name:
            return self.first_name.capitalize()

        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'


    def __repr__(self) -> str:
        return f"{self.email}"


from utils.rsa import RSAKeys

class RSAPair(models.Model):
    """ rsa key pairs """
    date_created = models.DateTimeField(auto_now_add=True)
    private_key = models.TextField(null=True, blank=True)
    public_key = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=1024, default="")
    
        
    def __str__(self) -> str:
        return f"{self.id}"
    
    def save(self, *args, **kwargs):
        
        keys = RSAKeys()
        
        from rest_framework_jwt.utils import uuid
        
        self.password = uuid.uuid1() 
        self.private_key = keys.private
        self.public_key = keys.public
        
        super(RSAPair, self).save(*args, **kwargs)
        
        
        
    
    