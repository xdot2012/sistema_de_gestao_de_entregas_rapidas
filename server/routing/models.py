from django.db import models
from meuapp.models import BaseModel


class Location(BaseModel):
    client = models.ForeignKey("legacy.Client", on_delete=models.CASCADE, related_name="location")
    address = models.CharField("Endereço", max_length=200)
    latitude = models.FloatField("Latitude")
    longitude = models.FloatField("Longitude")
    altitude = models.FloatField("Altitude")
