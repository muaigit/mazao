from django.db import models

# Create your models here.
class weather(models.Model):
    cityName=models.CharField(max_length=255)
    day=models.DateTimeField(auto_now_add=True)
    willitraintommorow=models.BooleanField()

    def __str__(self):
        return self.cityName
    
class SensorData(models.Model):
    temperature=models.IntegerField()
    humidity=models.IntegerField()
    moisture=models.IntegerField()
    time=models.DateTimeField(auto_now_add=True)
    irigate=models.BooleanField()
