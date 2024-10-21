from django.db import models
from django.utils import timezone

class Chat(models.Model):
    writer = models.CharField(default='', max_length=50)
    datetime = models.DateTimeField(default=timezone.now)
    content = models.TextField(default='')
    likers = models.JSONField(default=[])

    def __str__(self):
        return f'Chat sent by {self.writer} at {self.datetime}. He tells {self.content}'
    
    def __repr__(self):
        return f'Chat(writer={self.writer}, datetime={self.datetime}, content={self.content}, likers={self.likers}'

    def serialize(self):
        return {'writer': self.writer,
                'date': self.datetime.strftime("%b %d %Y, %I:%M %p"),
                'content': self.content,
                'likes': len(self.likers)}
