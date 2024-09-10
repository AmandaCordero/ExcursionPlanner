from django.db import models

class Point(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    height = models.FloatField()
    point_id = models.IntegerField(unique=True)
    characteristics = models.JSONField(default=list)

    def __str__(self):
        return f"Point({self.x}, {self.y}, point_id={self.point_id}"