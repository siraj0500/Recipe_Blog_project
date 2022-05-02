from django.db import models


class User_Message(models.Model):
    sender_name = models.CharField(max_length=50)
    sender_email = models.EmailField(max_length=70)
    sender_message = models.TextField(max_length=500)

    def __str__(self):
        return self.sender_name
