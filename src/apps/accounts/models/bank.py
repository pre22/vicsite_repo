from django.conf import settings
from django.db import models


class Balance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} || {self.user.email}"

# User crypto details are being stored here
class UserCryptoDetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    coin = models.CharField(max_length=400)
    wallet_address = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} || {self.user.email}"

class AmountInvested(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amt = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} || {self.user.email}"

class DueDate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(help_text="DD-MM-YYYY")

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} || {self.user.email}"