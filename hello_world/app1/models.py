from django.db import models

# Create your models here.
class Friends(models.Model):
  name = models.CharField(max_length=255)
  age = models.IntegerField()

  def __str__(self):
    # Define a tostring so that django admin shows the name properly.
    return self.name