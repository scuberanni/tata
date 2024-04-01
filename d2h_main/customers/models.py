from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class customer(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'Live'),(DELETE,'Delete'))
    name=models.CharField(max_length=50)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='costomer_profile')
    phone=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    