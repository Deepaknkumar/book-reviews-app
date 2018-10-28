from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    isbn = models.CharField(max_length=14, blank=False)
    title  = models.CharField(max_length=256, blank = False )
    author = models.CharField(max_length=256, blank = False)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.isbn} {self.title}({self.year}) by {self.author}"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name ="book")
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name ="user")
    rating = models.IntegerField(blank=False)
    review = models.TextField()

    class Meta:
        unique_together = ('book','user')
