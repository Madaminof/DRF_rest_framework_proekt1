from django.db import models

# Create your models here.


class Data(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    class Meta:
        db_table = 'data'

    def __str__(self):
        return f"{self.name} {self.id}"




