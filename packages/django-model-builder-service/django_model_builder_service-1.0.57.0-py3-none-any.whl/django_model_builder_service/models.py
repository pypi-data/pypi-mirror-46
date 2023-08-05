from django.db import models


# Create your models here.


class PredictionModel(models.Model):
    model = models.BinaryField()
    identifier = models.CharField(max_length=32)
    build_time = models.DateTimeField('build date')
    stats = models.TextField(name='stats', default='{}')
    build_duration = models.IntegerField(name='build_duration', default=0)
    config = models.TextField(name='config', default={})
    memory_usage = models.TextField(name='memory_usage', default='')

    def __str__(self):
        return '[{}] {}'.format(self.build_time, self.identifier)
