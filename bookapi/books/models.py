from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    release_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.author} ({self.release_year})'