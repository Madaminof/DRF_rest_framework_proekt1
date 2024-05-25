from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name


class ProductSigns(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    video = models.FileField(upload_to='videos/',null=True,blank=True)
    audio = models.FileField(upload_to='audio/',null=True,blank=True)
    doc = models.FileField(upload_to='doc/',null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_signs'


