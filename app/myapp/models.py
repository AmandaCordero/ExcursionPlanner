from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Point(models.Model):
    id = models.AutoField(primary_key=True)
    point_id = models.FloatField(unique=True)
    location_x = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],default=0.0)
    location_y = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],default=0.0)
    characteristics = models.JSONField(default=list)
    height = models.FloatField()

    def __str__(self):
        return f"Punto {self.point_id}"