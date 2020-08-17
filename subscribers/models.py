from django.db import models


class Subscriber(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=120)

    def __str__(self):
        return self.full_name
