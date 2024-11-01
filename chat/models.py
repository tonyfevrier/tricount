from django.db import models
from django.utils import timezone
 
class Chat(models.Model):
    writer = models.CharField(default='', max_length=50)
    #datetime = models.DateTimeField(default=timezone.now)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    content = models.TextField(default='')
    tricountid = models.IntegerField(default=0) 

    def __str__(self):
        return f'Chat sent by {self.writer} at {self.time} the {self.date}. He tells {self.content}'
    
    def __repr__(self):
        return f'Chat(writer={self.writer}, date={self.date}, time={self.time}, content={self.content}, tricountid={self.tricountid})'

    def serialize(self):
        return {'writer': self.writer,
                'date': self.date.strftime("%b %d %Y"),
                'time': self.time.strftime("%I:%M %p"),
                'content': self.content,
                'tricountid': self.tricountid} 
