from django.db import models
from django.forms import ValidationError

class Point(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    height = models.FloatField()
    point_id = models.IntegerField(unique=True)
    characteristics = models.JSONField(default=list)
    begin = models.BooleanField()
    finish = models.BooleanField()
    interesting = models.BooleanField()

    def __str__(self):
        return f"Point: {self.point_id}, location: ({self.x} ; {self.y})"
    
    def clean(self):
        if self.begin:
            if Point.objects.filter(begin=True).exclude(id=self.id).exists():
                raise ValidationError('Solo puede haber una entidad de Punto con begin en True.')
        if self.finish:
            if Point.objects.filter(finish=True).exclude(id=self.id).exists():
                raise ValidationError('Solo puede haber una entidad de Punto con finish en True.')

    def save(self, *args, **kwargs):
        self.clean()
        super(Point, self).save(*args, **kwargs)
    
class Edge(models.Model):
    point1 = models.ForeignKey(Point, related_name='edges_from', on_delete=models.CASCADE)
    point2 = models.ForeignKey(Point, related_name='edges_to', on_delete=models.CASCADE)
    distance = models.FloatField()
    characteristics = models.JSONField(default=list)

    class Meta:
        unique_together = ('point1', 'point2')

    def __str__(self):
        return f"Arista({self.point1.point_id} -> {self.point2.point_id})"
    
class Tourist(models.Model):
    name = models.CharField(unique=True, max_length=50)
    characteristics = models.JSONField(default=list)
    
    def __str__(self):
        return f"Nombre: {self.name}, Gustos: {self.characteristics})"
    