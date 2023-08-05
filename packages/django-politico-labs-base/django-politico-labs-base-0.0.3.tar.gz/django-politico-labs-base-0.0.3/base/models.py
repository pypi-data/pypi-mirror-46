from django.db import models


class HomepageLink(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.title
