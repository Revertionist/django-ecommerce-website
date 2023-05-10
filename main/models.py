from django.db import models

# Create your models here.
class product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField (max_length=100, null=False)
    description = models.TextField (null=False)
    image = models.ImageField(upload_to=None)