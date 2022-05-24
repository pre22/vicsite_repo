from django.db import models


class Coin(models.Model):
    coin_type = models.CharField(max_length=20)

    def __str__(self):
        return self.coin_type


# Address of the parent coin
class CoinAddress(models.Model):
    coin = models.ForeignKey('accounts.Coin', on_delete=models.CASCADE)
    coin_wallet_address = models.CharField(max_length=500)

    def __str__(self):
        return self.coin.coin_type