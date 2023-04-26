from django.db import models

# Create your models here.


class Menu(models.Model):

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()

    def __str__(self) -> str:
        return self.title


class Booking(models.Model):
    name = models.CharField(max_length=255)
    number_of_guest = models.IntegerField()
    booking_date = models.DateField()

    def __str__(self) -> str:
        return self.name
