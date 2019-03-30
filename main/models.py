from django.db import models

class Message(models.Model):

    def __init__(self, author, message, room, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author    # message author
        self.content = message  # message content(text)
        self.room = room        # from what chat room it comes

    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username
