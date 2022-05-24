from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models


class Contact(models.Model):
    c_email = models.EmailField(max_length=254)
    msg = models.CharField(max_length=50)

    def __str__(self):
        return self.c_email


class ProfilePic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    img = CloudinaryField('image')

    def __str__(self):
        return f'{self.user.firstname} {self.user.lastname} || {self.user.email}'