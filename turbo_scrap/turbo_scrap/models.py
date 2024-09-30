from django.db import models

class Post(models.Model):
    post_id = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.IntegerField()
    shares = models.IntegerField()
    comments = models.IntegerField()
    post_date = models.DateTimeField()

    def __str__(self):
        return self.post_id
